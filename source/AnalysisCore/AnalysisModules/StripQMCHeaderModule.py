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
from StripQMCHeaderPanel import *

class StripQMCHeaderModule( AnalysisModule ):
    def __init__(self):
        AnalysisModule.__init__(self, "Strip QMC Header")
        
    def checkModule( self, data ):
        return True
        
    def executeModule( self,data ):
            self.output = data

    def getInterfacePanel( self, parent, pipeline ):
        return StripQMCHeaderPanel( parent, self, pipeline )