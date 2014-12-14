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

import ScimitarModules
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

"""
Struct that contains various basic configuration settings for the run.
"""				
class RunSettings:
	def __init__( self ):
			self.scriptFilename = str( DEFAULT_SCRIPT_FILENAME )
			self.scriptLocation = str( DEFAULT_SCRIPT_LOCATION )
			self.executableFilename = str( DEFAULT_EXEC_FILENAME )
			self.inputFilename = str( DEFAULT_INPUT_FILENAME )
			self.outputFilename = str( DEFAULT_OUTPUT_FILENAME )
			self.sourcePath = str( DEFAULT_SOURCE_PATH )
			self.optionCompileSource = True
			self.optionBuildDirectoryStructure = True
			self.optionDisableInputRedirection = False
			self.optionGenerateCheckStatusScript = False

"""
Struct containing instantiations of all available modules.
"""
# Available so settings of each module can be maintained and written to file. These 
# modules should be activated in order to include them in the script.
class AvailableModules:
	def __init__(self, run):
		self.CreateDirectoryStructure = ScimitarModules.CreateDirectoryStructure( run )
		self.CompileSource = ScimitarModules.CompileSource( run )
		self.HeaderModule = ScimitarModules.HeaderModule( run )
		self.SingleMachineResourceManager = ScimitarModules.SingleMachineResourceManager( run )
		self.CheckStatus = ScimitarModules.CheckStatus( run )

"""
Definition class for a Scimitar run. This completely specifies the information
needed to construct an execution script.
"""			
class ScimitarRun:
	def __init__( self, species ):
		self.name = "DefaultRun"
		self.species = species
		self.runSettings = RunSettings()
		self.availableModules = AvailableModules( self )
		self.runNotes = ""
		
		# Active Scimitar modules.
		self.activeResourceManager = "NO_RESOURCE_MANAGER"
		self.activePreExecutionModules = []
		self.activePostExecutionModules = []
		
		# By default, set the active resource manager to be SingleMachine.
		self.activeResourceManager = self.availableModules.SingleMachineResourceManager
		
		# By default, activate all of the very important modules.
		self.activateModule( self.availableModules.HeaderModule )
		self.activateModule( self.availableModules.CompileSource )
		self.activateModule( self.availableModules.CreateDirectoryStructure )
		self.activateModule( self.availableModules.CheckStatus )
	
	"""
	Activate a Scimitar module.
	"""
	def activateModule( self, module ):
		if module.moduleType == ScimitarModules.ModuleTypes.ResourceManager:
			self.activeResourceManager = module
		elif module.moduleType == ScimitarModules.ModuleTypes.PreExecutionModule:
			self.activePreExecutionModules.append( module )
		elif module.moduleType == ScimitarModules.ModuleTypes.PostExecutionModule:
			self.activePostExecutionModules.append( module )
		else:
			raise ScimitarRunError( "Module '" + module.name + "' does not have a valid type." )
		
	"""
	Deactivate a Scimitar module. The object will still remain in AvailableModules.
	"""
	def deactivateModule( self, module ):
		if module.moduleType == ScimitarModules.ModuleTypes.ResourceManager:
			# Note that here we assume that we want the resource manager removed no matter
			# what (even if the passed resource manager does match the current one).
			self.activeResourceManager = "NO_RESOURCE_MANAGER"
		elif module.moduleType == ScimitarModules.ModuleTypes.PreExecutionModule:
			for i in range( 0, len( self.activePreExecutionModules ) ):
				if module == self.activePreExecutionModules[i]:
					del self.activePreExecutionModules[i]
					return
			raise ScimitarRunError( "Provided module is not active." )
		elif module.moduleType == ScimitarModules.ModuleTypes.PostExecutionModule:
			for i in range( 0, len( self.activePostExecutionModules ) ):
				if module == self.activePostExecutionModules[i]:
					del self.activePostExecutionModules[i]
					return
			raise ScimitarRunError( "Provided module is not active." )
		else:
			raise ScimitarRunError( "Module '" + module.name + "' does not have a valid type." )
		
	def isModuleActive( self, module ):
		if module in self.activePreExecutionModules:
			return True
		elif module in self.activePostExecutionModules:
			return True
		elif module == self.activeResourceManager:
			return True
		else:
			return False
		
	def getReportCard( self ):
		reportCard = "All grid checks passed!\n"
		reportCard += "Total number of runs: " + str( self.species.getRunCount() ) + "\n"
		return reportCard
		
	"""
	Generate the script for this run.
	"""
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
		if self.activeResourceManager == "NO_RESOURCE_MANAGER":
			raise ScimitarRunError( "There does not seem to be a valid resource manager loaded!")
			return
		script += self.activeResourceManager.getScriptContribution()
		
		# Load the post-execution module.
		for module in self.activePostExecutionModules:
			script += module.getScriptContribution()
			
		script += "\nprint '>> Scimitar execution script complete.'\n"
		return script