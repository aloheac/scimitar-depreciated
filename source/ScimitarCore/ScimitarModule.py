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

from enum import Enum

class ModuleTypes(Enum)
	GeneralModule = 0
	ResourceManager = 1
	PreExecutionModule = 2
	PostExecutionModule = 3
	
class ScimitarModule:
	def __init__( self, name, moduleType, priority, run ):
		self.moduleName = name
		self.moduleType = moduleType
		self.priority = priority
		self.run = run
		
	def getScriptContribution( self ):
		return "print Script contribution not implemented for module '" + self.name +  "'!"
		
		