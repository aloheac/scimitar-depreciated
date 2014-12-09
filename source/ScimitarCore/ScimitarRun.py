####################################################################
# Scimitar: ScimitarRun
#
# Class definition for a Scimitar run.
#
# Version 6.0
# 8 December 2014
#
# Joaquin E. Drut, Andrew C. Loheac
# Department of Physics and Astronomy
# University of North Carolina at Chapel Hill
####################################################################

DEFAULT_SCRIPT_FILENAME = "myscript.py"
DEFAULT_SCRIPT_LOCATION = "./"
DEFAULT_EXEC_FILENAME = "a.out"
DEFAULT_INPUT_FILENAME = "parameters.in"
DEFAULT_OUTPUT_FILENAME = "logfile.out"
DEFAULT_SOURCE_PATH = "../source"

"""
Generic Scimitar run exception.
"""
class ScimitarRunError( Exception ):
	def __init__( self, value ):
		self.value = value
		
	def __str__( self ):
		return repr( self.value )

class RunSettings:
	def __init__( self ):
			self.scriptFilename = str( DEFAULT_SCRIPT_FILENAME )
			self.scriptLocation = str( DEFAULT_SCRIPT_LOCATION )
			self.executableFilename = str( DEFAULT_EXEC_FILENAME )
			self.inputFilename = str( DEFAULT_INPUT_FILENAME )
			self.outputFilename = str( DEFAULT_OUTPUT_FILENAME )
			self.sourcePath = str( DEFAULT_SOURCE_PATH )
			self.optionCompileSource = 1
			self.optionBuildDirectoryStructure = 1
			self.optionDisableInputRedirection = 0
			
class ScimitarRun:
	def __init__( self, species ):
		self.name = "DefaultRun"
		self.species = species
		
		# Scimitar modules.
		self.loadedResourceManager = []
		self.loadedPreExecutionModules = []
		self.loadedPostExecutionModules = []
		self.inactiveResourceManagers = []
		self.inactivePreExecutionModules = []
		self.inactivePostExecutionModules = []
		
	def addModule( self, module ):
		pass
	
	def activateModule( self, module ):
		pass
		
	def deactivateModule( self, module ):
		pass
		
	def getRunCount( self ):
		pass
		
	def getReportCard( self ):
		pass