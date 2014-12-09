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

class SingleMachineResourceManager( ResourceManagerModule ):
	def __init__( self ):
		ResourceManagerModule.__init__( self, "Single Machine" )
		
	def getScriptContribution():
		if self.run.RunSettings.optionInputRedirection == 1:
			inputRedirection = " < "
		else:
			inputRedirection = " "
		
		return "./" self.run.RunSettings.executableFilename + inputRedirection \ 
		       + self.run.RunSettings.inputFilename + " > " \
		       + self.run.RunSettings.outputFilename