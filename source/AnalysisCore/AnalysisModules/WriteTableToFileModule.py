####################################################################
# Scimitar: AnalysisCoreModules: WriteTableToFileModule
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
from SplitTabularDataPanel import *

class WriteTableToFileModule( AnalysisModule ):
    def __init__(self):
        AnalysisModule.__init__(self, "Write Tabular Data to Disk")
        self.filePath = "D:/test_output.txt"
        self.output = None
        
    def checkModule( self, data ):
            return True
        
    def executeModule( self, data ):
        fileHandler = open( self.filePath, 'w' )
        
        for line in data:
            for word in line:
                fileHandler.write( word.strip() + ' ' )
            fileHandler.write( '\n' )
                
        fileHandler.close()
        
        self.output = data
        
    def getOutput(self):
        return self.output
                    
    def getInterfacePanel( self, parent ):
        return SplitTabularDataPanel( parent, self )