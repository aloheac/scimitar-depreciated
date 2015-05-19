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
        self.columnsToAverage = []
        self.output = None
        
    def checkModule( self, data ):
            return True
        
    def executeModule( self, data ):
        sums = []
        for column in self.columnsToAverage:
            sums.append( 0.0 )
        
        for i in range( 0, len( self.columnsToAverage ) ):
            for j in range( 0, len( data[ self.columnsToAverage[i] ] ) ):
                sums[i] += data[self.columnsToAverage[i]][j]
            sums[i] /= len( data[self.columnsToAverage[i]] )
        self.output = sums
        
    def getOutput(self):
        return self.output
                    
    def getInterfacePanel( self, parent ):
        return StripQMCHeaderPanel( parent, self )