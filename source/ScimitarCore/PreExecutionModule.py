####################################################################
# Scimitar: ScimitarModule:PreExecutionModule
#
# Class definition for a Scimitar pre-execution module.
#
# Version 6.0
# 8 December 2014
#
# Joaquin E. Drut, Andrew C. Loheac
# Department of Physics and Astronomy
# University of North Carolina at Chapel Hill
####################################################################

from ScimitarModule import *

class PreExecutionModule( ScimitarModule ):
	def __init__( self, name, priority, run ):
		ScimitarModule.__init__( self, name, ModuleTypes.PreExecutionModule, priority, run )
		
	def getScriptContribution( self ):
		return "print Script contribution not implemented for PreExecution module '" \
			   + self.name +  "'!"