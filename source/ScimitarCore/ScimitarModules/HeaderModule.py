####################################################################
# Scimitar: ScimitarModule:HeaderModule
#
# Very basic module that just prints out a heading.
#
# Version 6.0
# 8 December 2014
#
# Joaquin E. Drut, Andrew C. Loheac
# Department of Physics and Astronomy
# University of North Carolina at Chapel Hill
####################################################################

from PreExecutionModule import *

class HeaderModule( PreExecutionModule ):
	def __init__( self, run ):
		PreExecutionModule.__init__( self, "Header Module", 1, run )
		
	def getScriptContribution( self ):
		contribution  = "print ***************************************\n"
		contribution += "print * Scimitar Execution Script\n"
		contribution += "print * Version 6.0\n"
		contribution += "print ***************************************\n"
		return contribution