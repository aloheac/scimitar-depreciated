####################################################################
# Scimitar: AnalysisCoreModules: SplitTabularDataModule
#
# Module for splitting tabular data up into columns.
#
# Version 6.0
# 15 May 2015
#
# Joaquin E. Drut, Andrew C. Loheac
# Department of Physics and Astronomy
# University of North Carolina at Chapel Hill
####################################################################

from AnalysisCore.AnalysisModules.AnalysisModule import *
from AnalysisCore.AnalysisModules.SplitTabularDataPanel import *

class SplitTabularDataModule( AnalysisModule ):
    def __init__(self):
        AnalysisModule.__init__(self, "Split Tabular Data")
        
    def checkModule( self, data ):
            return True
        
    def executeModule( self, data ):
        for i in range( 0, len( data ) ):
            dataToBeSplit = data[i]
            newData = []
            for line in dataToBeSplit.splitlines():
                newData.append( line.strip().split( ' ' ) )
            data[i] = newData
        self.output = data
          
    def getInterfacePanel( self, parent, pipeline ):
        return SplitTabularDataPanel( parent, self, pipeline )