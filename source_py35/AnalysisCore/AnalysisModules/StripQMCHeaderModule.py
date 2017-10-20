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
from AnalysisCore.AnalysisModules.StripQMCHeaderPanel import *

class StripQMCHeaderModule( AnalysisModule ):
    def __init__(self):
        AnalysisModule.__init__(self, "Strip QMC Header")
        
    def checkModule( self, data ):
        return True
        
    def executeModule( self, data ):
        newData = []
        for i in range(0, len( data ) ):
            parsedData = []
            dataOutputReached = False
            for line in data[i].splitlines():
                words = line.split()
                if len( words ) > 0:
                    if dataOutputReached == True:
                        if len( words ) == 16:
                            parsedData.append( words )
                    else:
                        if words[0].strip() == "step":
                            dataOutputReached = True
            newData.append( parsedData )
        self.output = newData
    
    def getInterfacePanel( self, parent, pipeline ):
        return StripQMCHeaderPanel( parent, self, pipeline )