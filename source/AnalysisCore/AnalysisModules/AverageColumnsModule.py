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

from AnalysisModule import *
from StripQMCHeaderPanel import *

class AverageColumnsModule( AnalysisModule ):
    def __init__(self):
        AnalysisModule.__init__(self, "Average Columns")
        self.columnsToAverage = [0,1,2]
        self.output = None
        
    def checkModule( self, data ):
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
                    except ValueError:
                        raise ModuleExecutionError( "(AverageColumnsModule): Failed to convert a string to a float.")
                    sums[j] /= len( data[i] )
            self.output.append( sums )
        
    def getOutput(self):
        return self.output
                    
    def getInterfacePanel( self, parent ):
        return StripQMCHeaderPanel( parent, self )