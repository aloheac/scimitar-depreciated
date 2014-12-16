####################################################################
# Scimitar: ResourceManager:PBS
#
# Definition for the PBS resource manager (execution definition).
#
# Version 6.0
# 16 December 2014
#
# Joaquin E. Drut, Andrew C. Loheac
# Department of Physics and Astronomy
# University of North Carolina at Chapel Hill
####################################################################

from ResourceManagerModule import ResourceManagerModule

class PBSResourceManager( ResourceManagerModule ):
	def __init__( self, run ):
		ResourceManagerModule.__init__( self, "PBS", run )
		self.numNodes = 1
		self.processorsPerNode = 62
		self.walltime = "999:00:00"
		self.additionalPreExecutionCommands = ""
		self.additionalPostExecutionCommands = ""
		
	def getScriptContribution( self ):
		if self.run.runSettings.optionDisableInputRedirection == 0:
			inputRedirection = " < "
		else:
			inputRedirection = " "
		#TODO: Double check how to split newlines. Check that it works on tranquility. Check long string property types.
		contribution  = "\n# ***** ResourceManager: PBS *****\n"
		contribution += "from subprocess import Popen\n"
		contribution += "from time import sleep\n"
		contribution += "import os\n\n"
		contribution += "runListing = " + str( self.run.species.generateRunListing() ) + "\n"
		contribution += "jobCount = len( runListing )\n"
		contribution += "jobID = 0\n"
		contribution += "initialWorkingDir = os.path.dirname(os.path.abspath(__file__))\n\n"
		contribution += "print '>> Generating PBS scripts for each run...'\n"
		contribution += "for run in runListing:\n"
		contribution += "	os.chdir( initialWorkingDir += '/exec/' + run )\n"
		contribution += "	f_pbs_script = open( 'pbs_job_script.sub', 'w' )\n"
		contribution += "	f_pbs_script.write( '# Scimitar Generated PBS Job Submission Script' )\n"
		contribution += "	f_pbs_script.write( 'PBS -l nodes=" + str( self.numNodes ) + ":" + "ppn=" + str( self.processorsPerNode ) + "' )\n"
		contribution += "	f_pbs_script.write( 'PBS -l walltime=" + str( self.walltime ) + "' )\n"
		contribution += "	f_pbs_script.write( 'PBS -j oe\n' )\n"
		contribution += "	f_pbs_script.write( 'cd $PBS_O_WORKDIR' )\n"
		contribution += "# ***** End of ResourceManager: PBS *****\n\n"
		return contribution