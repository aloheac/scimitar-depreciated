####################################################################
# Scimitar: ScimitarModule:ResourceManagerModule
#
# Base class definition for a Scimitar resource manager module.
#
# Version 6.0
# 8 December 2014
#
# Joaquin E. Drut, Andrew C. Loheac
# Department of Physics and Astronomy
# University of North Carolina at Chapel Hill
####################################################################

from ScimitarModule import *

class ResourceManagerModule( ScimitarModule ):
	def __init__( self, name, run ):
		ScimitarModule.__init__( self, name, ModuleTypes.ResourceManager, 0, run )
		
	def getScriptContribution( self ):
		return "print Script contribution not implemented for ResourceManger module '" \
			   + self.name +  "'!"