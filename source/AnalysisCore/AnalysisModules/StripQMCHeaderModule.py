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

class StripQMCHeaderModule( AnalysisModule ):
    def __init__(self):
        AnalysisModule.__init__(self, "Strip QMC Header")
        
        def checkModule( data ):
            return True
        
        def executeModule( data ):
            self.output = data
