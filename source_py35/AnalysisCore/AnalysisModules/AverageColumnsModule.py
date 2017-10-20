####################################################################
# Scimitar: AnalysisCoreModules: 
#
# Module for writing tabular data to disk.
#
# Version 6.0
# 16 May 2015
#
# Joaquin E. Drut, Andrew C. Loheac
# Department of Physics and Astronomy
# University of North Carolina at Chapel Hill
####################################################################

from AnalysisCore.AnalysisModules.AnalysisModule import *
from AnalysisCore.AnalysisModules.StripQMCHeaderPanel import *

class AverageColumnsModule( AnalysisModule ):
    def __init__(self):
        AnalysisModule.__init__(self, "Average Columns")
        self.columnsToAverage = [0,1,2]
        self.output = None
        
    def checkModule( self, data ):
        if self.columnsToAverage == []:
            raise ModuleExecutionError( "(AverageColumns): Column list cannot be empty." )
        return True
        
    def executeModule( self, data ):
        self.output = []

        for i in range( 0, len( data ) ):
            sums = []
            for column in self.columnsToAverage:
                sums.append( 0.0 )
        
            for j in range( 0, len( self.columnsToAverage ) ):
                col = self.columnsToAverage[j]
                for k in range( 0, len( data[i] ) ):
                    try:
                        sums[j] += float( data[i][k][col] )
                    except (ValueError, TypeError):
                        raise ModuleExecutionError( "(AverageColumnsModule): Failed to convert a string to a float.")
                sums[j] /= len( data[i] )
            self.output.append( sums )
        
    def getOutput(self):
        return self.output
                    
    def getInterfacePanel( self, parent, pipeline ):
        return AverageColumnsPanel( parent, self, pipeline )
    
class AverageColumnsPanel( wx.Panel ):
    def __init__(self, parent, module, pipeline ):
        wx.Panel.__init__(self, parent )
        self.module = module
        self.pipeline = pipeline
        
        self.mainSizer = wx.BoxSizer( wx.VERTICAL )
        
        self.mainSizer.Add( wx.StaticText( self, label="Columns to average over (zero-indexed, list by commas):" ) )
        
        self.columnsTextEntry = wx.TextCtrl( self )
        self.mainSizer.Add( self.columnsTextEntry )
        
        self.btnUpdate = wx.Button( self, label="Update" )
        self.mainSizer.Add( self.btnUpdate )
        self.SetSizerAndFit( self.mainSizer )
        
        self.Bind( wx.EVT_BUTTON, self.onUpdate, self.btnUpdate )
        
    def onUpdate(self, evt):
        try:
            self.pipeline.columnsToAverage = []
            for element in self.columnsTextEntry.GetValue().split( ',' ):
                self.pipeline.columnsToAverage.append( float( element ) )
        except Exception as err:
            raise ModuleExecutionError( str( err ) )
        