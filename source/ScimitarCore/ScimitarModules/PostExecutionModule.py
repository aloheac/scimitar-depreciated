####################################################################
# Scimitar: ScimitarModule:PreExecutionModule
#
# Class definition for a Scimitar post-execution module.
#
# Version 6.0
# 8 December 2014
#
# Joaquin E. Drut, Andrew C. Loheac
# Department of Physics and Astronomy
# University of North Carolina at Chapel Hill
####################################################################

from ScimitarModule import *

class PostExecutionModule( ScimitarModule ):
	def __init__( self, name, priority ):
		ScimitarModule.__init__( self, name, ModuleTypes.PostExecutionModule, priority )
		
	def getScriptContribution( self ):
		return "print Script contribution not implemented for PostExecution module '" \
			   + self.name +  "'!"