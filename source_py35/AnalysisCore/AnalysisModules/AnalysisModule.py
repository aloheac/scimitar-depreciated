####################################################################
# Scimitar: AnalysisCore: AnalysisModule
#
# Abstract class for an analysis module.
#
# Version 6.0
# 15 May 2015
#
# Joaquin E. Drut, Andrew C. Loheac
# Department of Physics and Astronomy
# University of North Carolina at Chapel Hill
####################################################################

class ModuleExecutionError( Exception ):
    def __init__(self, value):
        self.value = value
        
    def __str__( self ):
        return repr( self.value )
    
class AnalysisModule():
    def __init__( self, moduleName ):
        self.moduleName = moduleName
        self.interfacePanel = None
        self.moduleID = None
        self.output = []
        
    def checkModule( self, data ):
        print( "Analysis module check not implemented for module " + self.moduleName + "!" )
            
    def executeModule( self, data ):
        print( "Analysis module execution not implemented for module " + self.moduleName + "!" )
        
    def getOutput( self ):
        return self.output
        
    def getInterfacePanel( self, parent, pipeline ):
        return None
        
        