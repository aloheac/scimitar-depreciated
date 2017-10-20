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

from ScimitarCore.ScimitarModules.ResourceManagerModule import ResourceManagerModule

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
		contribution  = "\n# ***** ResourceManager: Single Machine *****\n"
		
		# Import external packages.
		contribution += "from subprocess import Popen\n"
		contribution += "from time import sleep\n"
		contribution += "from datetime import datetime\n"
		contribution += "import os\n\n"
		
		# Initialized various variables and parameters. Note that the run
		# listing is given as a global variable at the beginning of the script.
		contribution += "jobCount = len( runListing )\n"
		contribution += "jobID = -1\n"
		contribution += "initialWorkingDir = os.path.dirname(os.path.abspath(__file__))\n\n"
		
		# Execute any pre-execution commands if there were any given.
		if not self.additionalPreExecutionCommands.strip() == "":
			contribution += "print '>> Executing additional pre-execution commands...'\n"
			contribution += "ADDITIONAL_PRE_EXEC_CMDS = " + str( self.additionalPreExecutionCommands.splitlines() ) + "\n"
			contribution += "for execLine in ADDITIONAL_PRE_EXEC_CMDS:\n"
			contribution += "	proc = Popen( execLine, shell=True )\n"
			contribution += "	proc.wait()\n"
			
		# Submit and run the jobs.
		contribution += "processDictionary = dict()\n"  # Dictionary between job IDs and PIDs.
		contribution += "print( '>> Submitting jobs (' + str( jobCount ) + ' total jobs)...' )\n"
		contribution += "runningJobs = []\n"
		contribution += "for run in runListing:\n"
		contribution += "	jobID +=1\n"
		contribution += "	print( '>>->> Submitting job no. ' + str( jobID + 1 ) + ' of ' + str( jobCount ) + ' [' + run + ']' )\n"
		contribution += "	os.chdir( initialWorkingDir + '/exec/' + run )\n"
		# If the job already completed and we are attempting a recovery, skip the job.
		contribution += "	if not os.path.isfile( './job_completed.tmp' ):\n"
		contribution += "		proc = Popen('./" + self.run.runSettings.executableFilename + inputRedirection + self.run.runSettings.inputFilename + " > " + self.run.runSettings.outputFilename + "', shell=True )\n"
		contribution += "		runningJobs.append( proc )\n"
		contribution += "		processDictionary[ proc.pid ] = jobID\n"
		contribution += "	else:\n"
		contribution += "		print( '>>->> Job has already completed.' )\n"
		
		# While we are running at the maximum number of jobs, keep checking for when other
		# jobs finish so we can launch another one.
		contribution += "	while len( runningJobs ) >= " + str( self.numSimRuns ) + ":\n"
		contribution += "		for process in runningJobs:\n"
		contribution += "			if process.poll() != None:\n"
		contribution += "				runningJobs.remove( process )\n"
		contribution += "				f_temp = open( initialWorkingDir + '/exec/' + runListing[ processDictionary[ process.pid ] ] + '/job_completed.tmp', 'w' )\n"
		contribution += "				f_temp.close()\n"
		contribution += "		sleep( " + str( self.procCheckWaitTime ) + " )\n"
		
		# After all jobs have been launched, wait for the last jobs to finish.
		contribution += "while len( runningJobs ) > 0:\n"
		contribution += "	for process in runningJobs:\n"
		contribution += "		if process.poll() != None:\n"
		contribution += "			runningJobs.remove( process )\n"
		contribution += "			f_temp = open( initialWorkingDir + '/exec/' + runListing[ processDictionary[ process.pid ] ] + '/job_completed.tmp', 'w' )\n"
		contribution += "			f_temp.close()\n"
		contribution += "	sleep( " + str( self.procCheckWaitTime ) + " )\n"
		
		# Run any additional post execution commands if there are any.
		if not self.additionalPostExecutionCommands.strip() == "":
			contribution += "print( '>> Executing additional post-execution commands...' )\n"
			contribution += "ADDITIONAL_POST_EXEC_CMDS = " + str( self.additionalPostExecutionCommands.splitlines() ) + "\n"
			contribution += "for execLine in ADDITIONAL_POST_EXEC_CMDS:\n"
			contribution += "	proc = Popen( execLine, shell=True )\n"
			contribution += "	proc.wait()\n"

		contribution += "print( '>> Execution completed at ' + str(datetime.now()) + '.' )\n"
		contribution += "# ***** End of ResourceManager: Single Machine *****\n\n"
		return contribution