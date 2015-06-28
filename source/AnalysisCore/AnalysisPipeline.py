####################################################################
# Scimitar: AnalysisCore: AnalysisPipeline
#
# Class definition for a Scimitar analysis pipeline.
#
# Version 6.0
# 15 May 2015
#
# Joaquin E. Drut, Andrew C. Loheac
# Department of Physics and Astronomy
# University of North Carolina at Chapel Hill
####################################################################

import AnalysisModules
import os.path
import os
import threading
from time import sleep
from wx import CallAfter, PyEvent, NewId, PostEvent

"""
Exception Class: Raised when an error is detected by the analysis pipeline
(generally in checking or executing modules).
"""
class AnalysisPipelineError( Exception ):
    def __init__( self, value ):
        self.value = value
        
    def __str__( self ):
        return repr( self.value )

"""
Generate a list of immediate subdirectories of a given directory.
dir: (string) Path of a directory to get the immediate subdirectories of.
"""
def _getListOfSubdirectories( dir ):
    listing = os.listdir( dir )   # Get immediate subdirectories only.
    subdirs = []
    for item in listing:
        if os.path.isdir( dir + '/' + item ):  # Ignore all items that are files.
            subdirs.append( item )
    return subdirs

"""
Generate a list of elements that were traversed from the head node of the
tree to the bottom leaf. Gives a list of all parameter values assigned
to a given run.
dir: (string) Head directory to begin traversal at.
"""
def _getTraversedParameterValues( dir ):
    subdirs = _getListOfSubdirectories( dir )
    
    if len( subdirs ) == 0:  # We are at the bottom of the directory tree.
        return []
    
    parameterValues = []
    for subdir in subdirs:
        # Note that the last element given by .split('_') is the parameter value. The head is the parameter name.
        parameterValues.append( [ subdir.split( '_' )[-1], _getTraversedParameterValues( dir + '/' + subdir ) ] )
            
    return parameterValues

"""
Generate a list of elements that were traversed from the head node of the
tree to the bottom leaf. Gives a list of all parameter names assigned to 
a given run. 
"""
def _getTraversedParameterNames( dir ):
    parameterNames = []
    atBottomOfDirTree = False
    currentDir = dir
    while not atBottomOfDirTree:
        subdirs = _getListOfSubdirectories( currentDir )
        if len( subdirs ) == 0:
            return parameterNames
        
        parameterNames.append( '_'.join( subdirs[0].split( '_' )[0:-1] ) )
        currentDir = currentDir + '/' + subdirs[0]

"""
Recursively count the number of leaves on a node with a root
element.
node: (Tree object) Tree to get the total number of leaves of.
"""
def numberOfLeaves( node ):
    if node[1] == []:
        return 1
    else:
        count = 0
        for child in node[1]:
            count += numberOfLeaves( child )
        return count
        
"""
Calculate the total number of runs associated with a given Scimitar directory
tree. This value is given by the total number of leaves in the tree.
"""
def _getTotalNumberOfRuns( dirTree ):
    count = 0
    for child in dirTree:
        count += numberOfLeaves( child )            
    return count

"""
TODO: Revisit how this works and comment!
"""
def _getRunParameterValues( runID, parameterNames, parameterValues ):
    def getTraversedValues( leafID, node ):
        if node[1] == []:
            return [node[0]]
        
        currentLeafID = leafID
        for child in node[1]:
            if currentLeafID < numberOfLeaves( child ):
                return[ node[0], getTraversedValues( leafID - currentLeafID, child ) ]
            else:
                currentLeafID -= numberOfLeaves( child )
                
    runValues = []
    currentRunID = runID   
    for child in parameterValues:
        if currentRunID < numberOfLeaves( child ):
            runValues = getTraversedValues( currentRunID, child )
            break
        else:
            currentRunID -= numberOfLeaves( child )
        
    flattenedRunValues = []
    for i in range(0, len( parameterNames ) - 1 ):
        flattenedRunValues.append( runValues[0] )
        runValues = runValues[1]
    flattenedRunValues.append( runValues[0] )
    
    runValues = []
    for i in range(0, len( parameterNames ) ):
        runValues.append( [ parameterNames[i], flattenedRunValues[i] ] )
        
    return runValues

"""
Get the run path relative to the head directory for a given run.
runID: (int) Index of the run to get the path of.
parameterNames: (list) List of the parameter names in order of the directory levels.
parameterValues: (nested list) Tree of the parameter values associated with all runs
                 as generated by _getRunParameterValues.
"""       
def _getRunPath( runID, parameterNames, parameterValues ):
    runValues = _getRunParameterValues(runID, parameterNames, parameterValues)
    
    path = "/"
    for i in range( 0, len( parameterNames ) ):
        path += str( parameterNames[i] ) + '_' + str( runValues[i][1] ) + '/'
    return path

"""
Load all the raw data for a Scimitar directory tree into a list ordered by run index.
pipeline: (AnalysisPipeline) Analysis pipeline to load the data into.
"""
def _getAllRawData( pipeline ):
    rawData = []
    numRuns = _getTotalNumberOfRuns( pipeline.parameterValueList )
    
    for i in range(0, numRuns):
        pipeline.eventProgress = int( 100 * i / numRuns )
        dataFilePath = str( pipeline.dataDirectory ) + _getRunPath( i, pipeline.parameterNameList, pipeline.parameterValueList) + str( pipeline.dataFilename )
        currentDataSet = ""

        try:
            file_handler = open( dataFilePath, 'r' )    
        except IOError:
            raise AnalysisPipelineError( "Data file '" + str( pipeline.dataDirectory ) + _getRunPath( i, pipeline.parameterNameList, pipeline.parameterValueList) + str( pipeline.dataFilename ) + "' does not exist." )
            pipeline.eventProgress = -1
            
        for line in file_handler:
            currentDataSet += line
        
        currentDataSet = [currentDataSet]    
        for module in pipeline.reductionModules:
            try:
                module.executeModule( currentDataSet )
            except AnalysisModules.ModuleExecutionError as err:
                raise AnalysisPipelineError( err.value )
                pipeline.eventProgress = -1
                
            currentDataSet = module.getOutput()
            
        rawData.append( currentDataSet[0] )
    pipeline.eventProgress = 0 
    pipeline.rawData = rawData


"""
Thread class for executing the analysis pipeline on a new thread. This allows
for a responsive UI when loading data files and executing modules.
"""
class PipelineExecutionThread( threading.Thread ):
    def __init__(self, threadID, pipeline):
        threading.Thread.__init__(self)
        
        # (int) Uniquely identifies this thread (not necessary for this application).
        self.threadID = threadID
        
        # Calling pipeline that launches this thread.
        self.pipeline = pipeline

    def run( self ):
        try:
            self.pipeline.loadRawData()
        except AnalysisPipelineError as err:
            PostEvent( self.pipeline.attachedUI.parent, ExecutionCompletedEvent( err, self.pipeline.EXECUTION_COMPLETE_ID ) )
            self.pipeline.eventProgress = -1
            return
        except Exception as err:
            PostEvent( self.pipeline.attachedUI.parent, ExecutionCompletedEvent( err, self.pipeline.EXECUTION_COMPLETE_ID ) )
            return
        
        numExecutedModules = 0
        returnedData = self.pipeline.rawData                
        for module in self.pipeline.activeModules:
            self.pipeline.eventProgress = int( 100 * float( numExecutedModules ) / float( len( self.pipeline.activeModules ) ) )
            try:
                module.executeModule( returnedData )
            except AnalysisModules.ModuleExecutionError as err:
                PostEvent( self.pipeline.attachedUI.parent, ExecutionCompletedEvent( err, self.pipeline.EXECUTION_COMPLETE_ID ) )
                self.pipeline.eventProgress = -1
                return
            except Exception as err:
                PostEvent( self.pipeline.attachedUI.parent, ExecutionCompletedEvent( err, self.pipeline.EXECUTION_COMPLETE_ID ) )
                return
            
            returnedData = module.getOutput()
            numExecutedModules += 1
        self.pipeline.rawData = returnedData
        self.pipeline.eventProgress = -1
        PostEvent( self.pipeline.attachedUI.parent, ExecutionCompletedEvent( None, self.pipeline.EXECUTION_COMPLETE_ID ) )
        
        # UI specific statements below. CallAfter call will execute these statements after
        # the thread terminates (I believe). UI will crash otherwise.
        CallAfter( self.pipeline.attachedUI.parent.loadDataTab.populateRunList )
        CallAfter( self.pipeline.attachedUI.parent.MainLog.WriteLogText, "Done." )
        CallAfter( self.pipeline.clearAttachedUI )  # Clear the attached UI so that it is not saved to file.


class ExecutionCompletedEvent( PyEvent ):
    def __init__(self, err, eventID):
        PyEvent.__init__(self)
        self.SetEventType( eventID )
        self.err = err
                                                        
"""
Main class for holding all state variables and methods associated with the analysis
pipeline.
"""    
class AnalysisPipeline:
    def __init__( self ):
        # Name of the pipeline.
        self.pipelineName = "Default Pipeline"
        
        # Parent Scimitar run directory to load all data from.
        self.dataDirectory = "./"
        
        # Name of the data file available in each leaf run directory that
        # will be loaded by the pipeline.
        self.dataFilename = "logfile.out"
        
        # List of loaded active analysis modules.
        self.activeModules = []
        
        # List of loaded inactive analysis modules.
        self.inactiveModules = []
        
        # List of loaded reduction analysis modules.
        self.reductionModules = []
        
        # Scimitar run data loaded from file. This array is updated after 
        # each module executes.
        self.rawData = []
        self.parameterNameList = []
        self.parameterValueList = []
        self._moduleID = 0
        self.eventProgress = 0
        self.attachedUI = None
        self.EXECUTION_COMPLETE_ID = NewId()
        
    def checkPipeline( self ):
            for module in self.reductionModules:
                module.checkModule( self.rawData )
        
            for module in self.activeModules:
                module.checkModule( self.rawData )
        
    def executePipeline( self ):
        executionThread = PipelineExecutionThread( 1, self )
        executionThread.start()
        
    def addReductionModule( self, module ):
        self.reductionModules.append( module )
                       
    def addActiveModule( self, module ):
        self.activeModules.append( module )
        
    def addInactiveModule( self, module ):
        self.inactiveModules.append( module )

    def removeModule( self , module ):
        for i in range(0, len( self.reductionModules ) ):
            if self.reductionModules[i] == module:
                    del self.reductionModules[i]   
                    return
                
        for i in range(0, len( self.activeModules ) ):
            if self.activeModules[i] == module:
                    del self.activeModules[i]   
                    return
         
        for i in range(0, len( self.inactiveModules ) ):
            if self.inactiveModules[i] == module:
                    del self.inactiveModules[i]   
                    return
                      
    def loadRawData( self ):
        if not os.path.isdir( self.dataDirectory ):
            raise AnalysisPipelineError( "Data directory '" + str( self.dataDirectory ) + "' does not exist." )   
            
        self.parameterNameList = _getTraversedParameterNames( self.dataDirectory )
        self.parameterValueList = _getTraversedParameterValues( self.dataDirectory )
            
        try:
            _getAllRawData( self )
        except AnalysisPipelineError as err:
            raise err
        
    def numberOfRuns(self):
        return _getTotalNumberOfRuns( self.parameterValueList )
    
    def getRunPath(self, runID):
        return _getRunPath( runID, self.parameterNameList, self.parameterValueList )
    
    def clearAttachedUI(self):
        self.attachedUI = None
        
    def getRunParameterValues( runID ):
    	return _getRunParameterValues( runID, self.parameterNames, self.parameterValues )