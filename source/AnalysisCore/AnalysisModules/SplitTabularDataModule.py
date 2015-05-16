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

from AnalysisModule import *
from SplitTabularDataPanel import *

class SplitTabularDataModule( AnalysisModule ):
    def __init__(self):
        AnalysisModule.__init__(self, "Split Tabular Data")
        
    def checkModule( self, data ):
            return True
        
    def executeModule( self, data ):
        for i in range( 0, len( data ) ):
            dataToBeSplit = data[i]
            data[i] = []
            for line in dataToBeSplit:
                data[i].append( line.split( ' ' ) )
                    
    def getInterfacePanel( self, parent ):
        return SplitTabularDataPanel( parent, self )