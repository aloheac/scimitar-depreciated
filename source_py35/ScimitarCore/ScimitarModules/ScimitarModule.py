####################################################################
# Scimitar: ScimitarModule
#
# Base class definition for a Scimitar module.
#
# Version 6.0
# 8 December 2014
#
# Joaquin E. Drut, Andrew C. Loheac
# Department of Physics and Astronomy
# University of North Carolina at Chapel Hill
####################################################################

class ModuleTypes:
	GeneralModule, ResourceManager, PreExecutionModule, PostExecutionModule = range( 4 )
	
class ScimitarModule:
	def __init__( self, name, moduleType, priority, run ):
		self.moduleName = name
		self.moduleType = moduleType
		self.priority = priority
		self.run = run
		
	def getScriptContribution( self ):
		return "print( \"Script contribution not implemented for module '" + self.name +  "'!\" )"
		
		