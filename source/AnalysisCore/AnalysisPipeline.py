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

class AnalysisPipelineError( Exception ):
    def __init__( self, value ):
        self.value = value
        
    def __str__( self ):
        return repr( self.value )

def _getListOfSubdirectories( dir ):
    listing = os.listdir( dir )
    subdirs = []
    for item in listing:
        if os.path.isdir( dir + '/' + item ):
            subdirs.append( item )
    return subdirs

def _getTraversedParameterValues( dir ):
    subdirs = _getListOfSubdirectories( dir )
    
    if len( subdirs ) == 0:  # We are at the bottom of the directory tree.
        return []
    
    parameterValues = []
    for subdir in subdirs:
        parameterValues.append( [ subdir.split( '_' )[-1], _getTraversedParameterValues( dir + '/' + subdir ) ] )
            
    return parameterValues

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

# Recursively count the number of leaves on a node with a root
# element.
def numberOfLeaves( node ):
    if node[1] == []:
        return 1
    else:
        count = 0
        for child in node[1]:
            count += numberOfLeaves( child )
        return count
        
def _getTotalNumberOfRuns( dirTree ):
    count = 0
    for child in dirTree:
        count += numberOfLeaves( child )            
    return count

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
       
def _getRunPath( runID, parameterNames, parameterValues ):
    runValues = _getRunParameterValues(runID, parameterNames, parameterValues)
    
    path = "/"
    for i in range( 0, len( parameterNames ) ):
        path += str( parameterNames[i] ) + '_' + str( runValues[i][1] ) + '/'
    return path

def _getAllRawData( parameterNames, parameterValues, dataDirectory, dataFilename ):
    rawData = []
    numRuns = _getTotalNumberOfRuns( parameterValues )
    
    for i in range(0, numRuns):
        dataFilePath = str( dataDirectory ) + _getRunPath( i, parameterNames, parameterValues) + str( dataFilename )
        currentDataSet = ""
        
        try:
            file_handler = open( dataFilePath, 'r' )    
        except IOError:
            raise AnalysisPipelineError( "Data file '" + str( dataDirectory ) + _getRunPath( i, parameterNames, parameterValues) + str( dataFilename ) + "' does not exist." )
        
        for line in file_handler:
            currentDataSet += line
    
        rawData.append( currentDataSet )
        
    return rawData
    
class AnalysisPipeline:
    def __init__( self ):
        self.pipelineName = "Default Pipeline"
        self.dataDirectory = "./"
        self.dataFilename = "logfile.out"
        self.activeModules = []
        self.inactiveModules = []
        self.reductionModules = []
        self.rawData = []
        self.parameterNameList = []
        self.parameterValueList = []
        self._moduleID = 0
        
    def checkPipeline( self ):
            for module in self.reductionModules:
                module.checkModule()
        
            for module in self.activeModules:
                module.checkModule()
        
    def executePipeline( self ):
            returnedData = self.rawData
            
            for module in self.reductionModules:
                for i in range(0, len( self.rawData ) ):
                    module.executeModule( returnedData[i] )
                    returnedData[i] = module.getOutput()
                    
            for module in self.activeModules:
                module.executeModule( returnedData )
                returnedData = module.getOutput()
                
            return returnedData
    
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
            
        self.rawData = _getAllRawData( self.parameterNameList, self.parameterValueList, self.dataDirectory, self.dataFilename )
        
    def numberOfRuns(self):
        return _getTotalNumberOfRuns( self.parameterValueList )
    
    def getRunPath(self, runID):
        return _getRunPath( runID, self.parameterNameList, self.parameterValueList )