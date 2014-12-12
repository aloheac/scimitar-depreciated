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

from PreExecutionModule import PreExecutionModule

# Standard Fortran-style input file.
def _createInputFileForRun( self, run, parameterList, valueList ):
	run = run.split('/')
	splitRuns = []
	for r in run:
		splitRuns.append( r.split('_') )
		
class CreateDirectoryStructure( PreExecutionModule ):
	def __init__( self, run ):
		PreExecutionModule.__init__( self, "Create Directory Structure", 1, run )
	
	def getScriptContribution( self ):
		contribution  = "# ***** PreExecution: Create Directory Structure *****\n"
		contribution += "# ***** End of PreExecution: Create Directory Structure *****\n"
		return contribution