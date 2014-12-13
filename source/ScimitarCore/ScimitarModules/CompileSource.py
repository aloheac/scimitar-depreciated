####################################################################
# Scimitar: ScimitarModule:PreExecution:CompileSource
#
# Module that builds source and copies it to the run directory.
#
# Version 6.0
# 8 December 2014
#
# Joaquin E. Drut, Andrew C. Loheac
# Department of Physics and Astronomy
# University of North Carolina at Chapel Hill
####################################################################

from PreExecutionModule import PreExecutionModule

class CompileSource( PreExecutionModule ):
	def __init__( self, run ):
		PreExecutionModule.__init__( self, "Compile Source", 10, run )
		
	def getScriptContribution( self ):
		if self.run.runSettings.optionCompileSource:
			contribution  = "# ***** Pre Execution: Compile Source *****\n"
			contribution += "from subprocess import Popen\n"
			contribution += "import os\n"
			contribution += "print '>> Compiling executable from source...'\n"
			contribution += "initWorkingDir = os.path.dirname(os.path.abspath(__file__))\n"
			contribution += "os.chdir('" + self.run.runSettings.sourcePath + "')\n"
			contribution += "proc = Popen('make clean', shell=True)\n"
			contribution += "proc.wait()\n"
			contribution += "proc = Popen('make', shell=True)\n"
			contribution += "proc.wait()\n"
			contribution += "os.chdir(initWorkingDir)\n"
			contribution += "proc = Popen('cp " + self.run.runSettings.sourcePath + "/" + self.run.runSettings.executableFilename + " .', shell=True)\n"
			contribution += "proc.wait()\n"
			contribution += "# ***** End of Compile Source *****\n\n"
		
		return contribution