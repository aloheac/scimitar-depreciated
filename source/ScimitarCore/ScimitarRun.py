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

from ScimitarModules import *
from ScimitarSpecies import *

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

# Alright, I don't know how to write comparators in Python so let's just do it the
# crappy way for now. These lists won't get too long anyway.
def _sortModuleList( moduleList ):
	# Yes, this is bubble sort. No, I didn't feel like being smart.
	for i in range( 0, len( moduleList ) ):
		for j in range( len( moduleList ) - 1, i, -1 ):
			if moduleList[ j ].priority < moduleList[ j - 1 ].priority:
				moduleList[ j ], moduleList[ j-1 ] = moduleList[ j-1 ], moduleList[ j ]
				
# Just a struct containing a bunch of configuration settings.
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
		self.runSettings = RunSettings()
		
		# Scimitar modules.
		self.activeResourceManager = "NO_RESOURCE_MANAGER"
		self.activePreExecutionModules = []
		self.activePostExecutionModules = []
	
	def activateModule( self, module ):
		if module.moduleType == ModuleTypes.ResourceManager:
			self.activeResourceManager = module
		elif module.moduleType == ModuleTypes.PreExecutionModule:
			self.activePreExecutionModules.append( module )
		elif module.moduleType == ModuleTypes.postExecutionModule:
			self.activePostExecutionModules.append( module )
		else:
			raise ScimitarRunError( "Module '" + module.name + "' does not have a valid type." )
		
	def deactivateModule( self, module ):
		if module.moduleType == ModuleTypes.ResourceManager:
			# Note that here we assume that we want the resource manager removed no matter
			# what (even if the passed resource manager does match the current one).
			self.activeResourceManager = "NO_RESOURCE_MANAGER"
		elif module.moduleType == ModuleTypes.PreExecutionModule:
			for i in range( 0, len( self.activePreExecutionModules ) ):
				if module == self.activePreExecutionModules[i]:
					del self.activePreExecutionModules[i]
					return
			raise ScimitarRunError( "Provided module is not active." )
		elif module.moduleType == ModuleTypes.postExecutionModule:
			for i in range( 0, len( self.activePostExecutionModules ) ):
				if module == self.activePostExecutionModules[i]:
					del self.activePostExecutionModules[i]
					return
			raise ScimitarRunError( "Provided module is not active." )
		else:
			raise ScimitarRunError( "Module '" + module.name + "' does not have a valid type." )
		
	def getReportCard( self ):
		pass
		
	def generateScript( self ):
		# Start with an empty script.
		script = ""
		
		# Sort the execution modules by priority.
		_sortModuleList( self.activePreExecutionModules )
		_sortModuleList( self.activePostExecutionModules )
		
		# Load the pre-execution module.
		for module in self.activePreExecutionModules:
			script += module.getScriptContribution()
		
		# Load the execution module.
		script += self.activeResourceManager.getScriptContribution()
		
		# Load the post-execution module.
		for module in self.activePostExecutionModules:
			script += module.getScriptContribution()
			
		script += "print >> Scimitar execution script complete.\n"
		return script