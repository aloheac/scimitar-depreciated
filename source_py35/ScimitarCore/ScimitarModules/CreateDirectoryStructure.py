####################################################################
# Scimitar: ScimitarModule:HeaderModule
#
# Very basic module that just prints out a heading.
#
# Version 6.0
# 13 December 2014
#
# Joaquin E. Drut, Andrew C. Loheac, Dhruv K. Mittal
# Department of Physics and Astronomy
# University of North Carolina at Chapel Hill
####################################################################

from ScimitarCore.ScimitarModules.PreExecutionModule import PreExecutionModule

def _getParameterList( run ):
	parameterList = []
	for i in range( 0, run.species.numRows ):
		parameterList.append( run.species.getElement( i, 0 ) )
	return str( parameterList )

def _getValueList( run ):
	valueList = []
	for i in range( 0, run.species.numRows ):
		valueList.append( run.species.getElement( i, 2 ) )
	return str( valueList )


def _getFormatList( run ):
	formatList = []
	for i in range( 0, run.species.numRows ):
		element = run.species.getElement( i, 4 )
		if element.strip() == "--" or element.strip() == "":
			formatList.append( "{}" )
		else:
			formatList.append( "{:" + element.strip() + "}" )

	return str( formatList )

class CreateDirectoryStructure( PreExecutionModule ):
	def __init__( self, run ):
		PreExecutionModule.__init__( self, "Create Directory Structure", 20, run )
	
	def getScriptContribution( self ):
		contribution  = "# ***** PreExecution: Create Directory Structure *****\n"
		
		# Import external modules.
		contribution += 'from subprocess import Popen\n'
		contribution += 'import os\n\n'

		# Private function for generating input file for a run.
		contribution += "def _createInputFileForRun( run, parameterList, valueList, formatList ):\n"
		contribution += "	run = run.split('/')\n"
		contribution += "	uniqueParams = []\n"
		contribution += "	for pair in run:\n"
		contribution += "		pair_s = pair.split('_')\n"
		contribution += "		parameterName = '_'.join(pair_s[0:-1])\n"
		contribution += "		uniqueParams.append( (parameterName, pair_s[-1]) )\n\n"
		contribution += "	inputFile = ''\n"
		contribution += "	for i in range( 0, len( parameterList ) ):\n"
		contribution += "		value = None\n"
		contribution += "		for j in range( 0, len( uniqueParams ) ):\n"
		contribution += "			if uniqueParams[j][0] == parameterList[i]:\n"
		contribution += "				value = uniqueParams[j][1]\n"
		contribution += "				break\n"

		contribution += "		if value == None:\n"
		contribution += "			value = str( formatList[i] ).format( valueList[i] )\n\n"
		contribution += "		inputFile += value + '\t#' + parameterList[i] + '\\n'\n"
		contribution +=	"	return inputFile\n\n"
		
		# Initialize parameters. Recall that the run listing is given as a global variable.
		contribution += "parameterList = " + _getParameterList( self.run ) + "\n"
		contribution += "valueList = " + _getValueList( self.run ) + "\n"
		contribution += "formatList = " + _getFormatList( self.run ) + "\n"
		contribution += "initWorkingDir = os.path.dirname( os.path.abspath(__file__) )\n"
		contribution += "okayToCreateDirectoryStructure = True\n"
		
		# Check if the execution directory structure already exists. If is does, show a 
		# warning to the user and let them decide if they should continue.
		contribution += "if os.path.isdir( initWorkingDir + '/exec/' ):\n"
		contribution += "	print( '>> WARNING: It appears that an execution directory structure already exists,' )\n"
		contribution += "	print( '            and will not be recreated unless it is first removed. This script' )\n"
		contribution += "	print( '            may overwrite existing data. If you are restarting a run after it' )\n"
		contribution += "	print( '            aborted, please continue.' )\n"
		contribution += "	while True:\n"
		contribution += "		userResponse = input( 'Do you want to continue running the script? (y/n): ' )\n"
		contribution += "		if userResponse == 'y':\n"
		contribution += "			okayToCreateDirectoryStructure = False\n"
		contribution += "			print( '>> Continuing the script with the existing directory structure.' )\n"
		contribution += "			break\n"
		contribution += "		elif userResponse == 'n':\n"
		contribution += "			print( '>> Terminating the script at the user\\'s request.' )\n"
		contribution += "			raise SystemExit\n"
		
		# Build and populate the directory structure.
		contribution += "if okayToCreateDirectoryStructure:\n"
		if self.run.runSettings.optionBuildDirectoryStructure:
			contribution += "	print( '>> Creating directory structure...' )\n"
			contribution += "	for run in runListing:\n"
			contribution += "		os.makedirs( initWorkingDir + '/exec/' + run )\n"
		contribution += "	print( '>> Generating input files and copying executable...' )\n"
		contribution += "	for run in runListing:\n"
		contribution += "		os.chdir( initWorkingDir + '/exec/' + run )\n"
		contribution += "		f_inputFile = open( initWorkingDir + '/exec/' + run + '/" + self.run.runSettings.inputFilename + "', 'w' )\n"
		contribution += "		f_inputFile.write( _createInputFileForRun( run, parameterList, valueList, formatList ) )\n"
		contribution += "		f_inputFile.close()\n"
		contribution += "		if not os.path.isfile( initWorkingDir + '/" + self.run.runSettings.executableFilename + "'):\n"
		contribution += "			if os.path.isfile( '" + self.run.runSettings.sourcePath + "/" + self.run.runSettings.executableFilename + "' ):\n"
		contribution += "				print( '>> NOTE: The executable was not found in the current directory. Copying the existing executable from the source directory.' )\n"
		contribution += "				proc = Popen( 'cp " + self.run.runSettings.sourcePath + "/" + self.run.runSettings.executableFilename + " ' + initWorkingDir + '/" + self.run.runSettings.executableFilename + "', shell=True )\n"
		contribution += "				proc.wait()\n"
		contribution += "			else:\n"
		contribution += "				print( '>> ERROR: The executable could not be found. The source may have not compiled successfully.' )\n"
		contribution += "				raise SystemExit\n"
		contribution += "		proc = Popen( 'cp ' + initWorkingDir + '/" + self.run.runSettings.executableFilename + " .', shell=True )\n"
		contribution += "		proc.wait()\n"
		contribution += "	os.chdir( initWorkingDir )\n"
		contribution += "# ***** End of PreExecution: Create Directory Structure *****\n"
		return contribution
