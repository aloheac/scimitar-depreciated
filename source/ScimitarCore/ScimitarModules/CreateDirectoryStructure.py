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
	
class CreateDirectoryStructure( PreExecutionModule ):
	def __init__( self, run ):
		PreExecutionModule.__init__( self, "Create Directory Structure", 20, run )
	
	def getScriptContribution( self ):
		contribution  = "# ***** PreExecution: Create Directory Structure *****\n"
		contribution += 'from subprocess import Popen\n'
		contribution += 'import os\n\n'
		contribution += "def _createInputFileForRun( run, parameterList, valueList ):\n"
		contribution += "	run = run.split('/')\n"
		contribution +=	"	splitRuns = []\n"
		contribution += "	for r in run:\n"
		contribution += "		splitRuns.append( r.split('_') )\n"
		contribution += "		inputFile = ''\n"	
		contribution += "		for i in range( 0, len( parameterList ) ):\n"
		contribution += "			valueToAdd = ''\n"
		contribution += "			parameterToAdd = ''\n"
		contribution += "			for j in range( 0, len( splitRuns ) ):\n"
		contribution += "				if parameterList[i] == splitRuns[j][0]:\n"
		contribution += "					parameterToAdd = str( parameterList[i] )\n"
		contribution += "					valueToAdd = str( splitRuns[j][1] )\n"
		contribution += "					break\n"
		contribution += "			if valueToAdd == '' and parameterToAdd == '':\n"
		contribution += "				inputFile += str( valueList[i] ) + '\t#' + str( parameterList[i] ) + '\\n'\n"
		contribution += "			else:\n"
		contribution += "				inputFile += valueToAdd + '\t#' + parameterToAdd + '\\n'\n"
		contribution +=	"	return inputFile\n\n"
		contribution += "runListing = " + str( self.run.species.generateRunListing() ) + "\n"
		contribution += "parameterList = " + _getParameterList( self.run ) + "\n"
		contribution += "valueList = " + _getValueList( self.run ) + "\n"
		contribution += "initWorkingDir = os.path.dirname( os.path.abspath(__file__) )\n"
		if self.run.runSettings.optionBuildDirectoryStructure:
			contribution += "print '>> Creating directory structure...'\n"
			contribution += "for run in runListing:\n"
			contribution += "	os.makedirs( initWorkingDir + '/exec/' + run )\n"
		contribution += "print '>> Generating input files and copying executable...'\n"
		contribution += "for run in runListing:\n"
		contribution += "	os.chdir( initWorkingDir + '/exec/' + run )\n"
		contribution += "	f_inputFile = open( initWorkingDir + '/exec/' + run + '/" + self.run.runSettings.inputFilename + "', 'w' )\n"
		contribution += "	f_inputFile.write( _createInputFileForRun( run, parameterList, valueList ) )\n"
		contribution += "	f_inputFile.close()\n"
		contribution += "	if not os.path.isfile( initWorkingDir + '/" + self.run.runSettings.executableFilename + "'):\n"
		contribution += "		print '>> ERROR: The executable does not exist in the same directory as the script. The source may have not compiled successfully.'\n"
		contribution += "		raise SystemExit\n"
		contribution += "	proc = Popen( 'cp ' + initWorkingDir + '/" + self.run.runSettings.executableFilename + " .', shell=True )\n"
		contribution += "	proc.wait()\n"
		contribution += "os.chdir( initWorkingDir )"
		contribution += "# ***** End of PreExecution: Create Directory Structure *****\n"
		return contribution