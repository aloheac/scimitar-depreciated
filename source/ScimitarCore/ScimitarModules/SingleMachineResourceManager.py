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
		self.numSimRuns = 62
		self.procCheckWaitTime = 5
		self.additionalPreExecutionCommands = ""
		self.additionalPostExecutionCommands = ""
		
	def getScriptContribution( self ):
		if self.run.runSettings.optionDisableInputRedirection == 0:
			inputRedirection = " < "
		else:
			inputRedirection = " "
		#TODO: Double check how to split newlines. Check that it works on tranquility. Check long string property types.
		contribution  = "\n# ***** ResourceManager: Single Machine *****\n"
		contribution += "from subprocess import Popen\n"
		contribution += "from time import sleep\n"
		contribution += "import os\n\n"
		contribution += "runListing = " + str( self.run.species.generateRunListing() ) + "\n"
		contribution += "jobCount = len( runListing )\n"
		contribution += "jobID = 0\n"
		contribution += "initialWorkingDir = os.path.dirname(os.path.abspath(__file__))\n\n"
		if not self.additionalPreExecutionCommands.strip() == "":
			contribution += "print '>> Executing additional pre-execution commands...'\n"
			contribution += "ADDITIONAL_PRE_EXEC_CMDS = " + str( self.additionalPreExecutionCommands.splitlines() ) + "\n"
			contribution += "for execLine in ADDITIONAL_PRE_EXEC_CMDS:\n"
			contribution += "	proc = Popen( execLine, shell=True )\n"
			contribution += "	proc.wait()\n"
		contribution += "print '>> Submitting jobs (' + str( jobCount ) + ' total jobs)...'\n"
		contribution += "runningJobs = []\n"
		contribution += "for run in runListing:\n"
		contribution += "	jobID +=1\n"
		contribution += "	print '>>->> Submitting job no. ' + str( jobID ) + ' of ' + str( jobCount ) + ' [' + run + ']'\n"
		contribution += "	os.chdir( initialWorkingDir + '/exec/' + run )\n"
		contribution += "	proc = Popen('./" + self.run.runSettings.executableFilename + inputRedirection + self.run.runSettings.inputFilename + " >> " + self.run.runSettings.outputFilename + "', shell=True )\n"
		contribution += "	runningJobs.append( proc )\n"
		contribution += "	for process in runningJobs:\n"
		contribution += "		if process.poll() != None:\n"
		contribution += "			runningJobs.remove( process )\n"
		contribution += "	while len( runningJobs ) >= " + str( self.numSimRuns ) + ":\n"
		contribution += "		runningJobs.append( proc )\n"
		contribution += "		for process in runningJobs:\n"
		contribution += "			if process.poll() != None:\n"
		contribution += "				runningJobs.remove( process )\n"
		contribution += "		sleep( " + str( self.procCheckWaitTime ) + " )\n"
		if not self.additionalPostExecutionCommands.strip() == "":
			contribution += "print '>> Executing additional post-execution commands...'\n"
			contribution += "ADDITIONAL_POST_EXEC_CMDS = " + str( self.additionalPostExecutionCommands.splitlines() ) + "\n"
			contribution += "for execLine in ADDITIONAL_POST_EXEC_CMDS:\n"
			contribution += "	proc = Popen( execLine, shell=True )\n"
			contribution += "	proc.wait()\n"
		contribution += "# ***** End of ResourceManager: Single Machine *****\n\n"
		return contribution