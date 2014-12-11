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

from ResourceManagerModule import ResourceManagerModule

class SingleMachineResourceManager( ResourceManagerModule ):
	def __init__( self, run ):
		ResourceManagerModule.__init__( self, "Single Machine", run )
		self.optionSimRuns = 62
		self.procCheckWaitTime = 5
		
	def getScriptContribution( self ):
		if self.run.runSettings.optionDisableInputRedirection == 0:
			inputRedirection = " < "
		else:
			inputRedirection = " "
		
		contribution  = "\n# ***** ResourceManager: Single Machine *****\n"
		contribution += "from subprocess import Popen\n"
		contribution += "from time import sleep\n"
		contribution += "import os\n\n"
		contribution += "runListing = " + str( self.run.species.generateRunListing() ) + "\n"
		contribution += "jobCount = len( runListing )\n"
		contribution += "jobID = 0\n"
		contribution += "initialWorkingDir = os.path.dirname(os.path.abspath(__file__))\n\n"
		contribution += "print '>> Submitting jobs (' + str( jobCount ) + ' total jobs)...'\n"
		contribution += "runningJobs = []\n"
		contribution += "for run in runListing:\n"
		contribution += "	jobID +=1\n"
		contribution += "	print '>>->> Submitting job no. ' + str( jobID ) + ' of ' + str( jobCount ) + ' [' + run + ']'\n"
		contribution += "	os.chdir( initialWorkingDir + run )\n"
		contribution += "	proc = Popen('./" + self.run.runSettings.executableFilename + inputRedirection + self.run.runSettings.inputFilename + " >> " + self.run.runSettings.outputFilename + "', shell=True )\n"
		contribution += "	runningJobs.append( proc )\n"
		contribution += "	for process in runningJobs:\n"
		contribution += "		if process[0].poll() != None:\n"
		contribution += "			runningJobs.remove( process )\n"
		contribution += "	while len( runningJobs ) > " + str( self.optionSimRuns ) + ":\n"
		contribution += "		runningJobs.append( proc )\n"
		contribution += "		for process in runningJobs:\n"
		contribution += "			if process[0].poll() != None:\n"
		contribution += "				runningJobs.remove( process )\n"
		contribution += "		sleep( " + str( self.procCheckWaitTime ) + " )\n"
		contribution += "# ***** End of ResourceManager: Single Machine *****\n\n"
		return contribution