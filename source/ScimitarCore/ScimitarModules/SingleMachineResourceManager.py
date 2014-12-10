####################################################################
# Scimitar: ResourceManager:SingleMachine
#
# Definition for the single machine resource manager (execution definition).
#
# Version 6.0
# 8 December 2014
#
# Joaquin E. Drut, Andrew C. Loheac
# Department of Physics and Astronomy
# University of North Carolina at Chapel Hill
####################################################################

from ResourceManagerModule import *

class SingleMachineResourceManager( ResourceManagerModule ):
	def __init__( self, run ):
		ResourceManagerModule.__init__( self, "Single Machine", run )
		self.optionSimRuns = 64
		
	def getScriptContribution( self ):
		if self.run.runSettings.optionDisableInputRedirection == 0:
			inputRedirection = " < "
		else:
			inputRedirection = " "
		
		contribution  = "from subprocess import Popen\n"
		contribution += ""
		return "proc = Popen(./" + self.run.runSettings.executableFilename + inputRedirection + self.run.runSettings.inputFilename + " > " + self.run.runSettings.outputFilename + ", shell=True)\n"