####################################################################
# Scimitar: ScimitarSpecies
#
# Class definition for a Scimitar species.
#
# Version 6.0
# 8 December 2014
#
# Joaquin E. Drut, Andrew C. Loheac
# Department of Physics and Astronomy
# University of North Carolina at Chapel Hill
####################################################################

DEFAULT_NUM_ROWS = 3
DEFAULT_NUM_COLUMNS = 4
DEFAULT_EMPTY_ELEMENT = '--'

"""
Standard exception that will be raised by ScimitarSpecies if an error is detected in
checkGrid().
"""
class ScimitarGridError( Exception ):
	def __init__( self, value ):
		self.value = value
		
	def __str__( self ):
		return repr( self.value )

"""
Exception that will be raised if a general error is encountered (i.e. index bounds).
"""	
class ScimitarSpeciesError( Exception ):
	def __init__( self, value ):
		self.value = value
		
	def __str__( self ):
		return repr( self.value )

"""
Given a value entered into the grid, return a list of the expanded structure (i.e.
expand all ranges and functions).
"""
# ASSERTION: All values are valid and of the matching type.	
def _expandValues( value, type ):
	if type == "int" or type == "real":
		# Something could be a list: 1,2,3,4.
		return value.split(',')
	if type == "range":
		allValues = []	
		# Something could be a list of ranges: 1:0.5:3,5:0.1:7.
		splitRanges = value.split(',')
		for splitRange in splitRanges:
			minimum = float( splitRange.split(':')[0] )
			step = float( splitRange.split(':')[1] )
			maximum = float( splitRange.split(':')[2] )
			while minimum <= maximum:
				allValues.append( minimum )
				minimum += step
		return allValues

"""
Check if a range value is valid.
"""
def _isValidRange( value ):
	nums = value.split( ':' )
	for i in range( 0, 2 ):
		try:
			float( nums[i] )
		except ValueError:
			return False
	return True

"""
Species object for Scimitar. This should only directly be used by the core.
"""
class ScimitarSpecies:
		"""
		Default constructor.
		"""	
		def __init__( self ):
			# The name of the species.
			self.name = "DefaultSpecies"
		
			# Grid dimensions of the species.
			self.numRows = DEFAULT_NUM_ROWS;
			self.numColumns = DEFAULT_NUM_COLUMNS;
			
			# const: Names of the grid headings of the Species.
			self.speciesHeadings = [ "Parameter", "Type", "Value", "Dir Order", "Notes" ]

			# Initialize grid of parameters to the default.	Note that the two
			# dimensional list is row-major.
			self.parameterGrid = []
			emptyRow = []
			# For each field in a row, add the default empty string to the list.
			for i in range( 0, DEFAULT_NUM_COLUMNS ):
				emptyRow.append( str( DEFAULT_EMPTY_ELEMENT ) )
			for j in range( 0, DEFAULT_NUM_ROWS ):
				self.parameterGrid.append( list( emptyRow ) )
			self.parameterGrid = [['a', 'int', '5', '1'],['b','range','1:1:10','2'],['c','real','6,7,8,9','3']]
		
		"""
		Add a blank row to the parameter grid of the species.
		"""
		def addRow( self, numRowBefore ):
			# Make sure the given index is valid, if not raise an exception.
			if numRowBefore >= self.numRows:
				raise ScimitarSpeciesError( 'Index of row to add a new row after is out of range!' )
				return
		
			# Increment the row dimensions by one.
			self.numRows += 1
			
			# Generate a list that is an empty row.
			emptyRow = []
			for i in range( 1, self.numColumns ):
				emptyRow.append( str( DEFAULT_EMPTY_ELEMENT ) )
				
			# Insert the new row into the two-dimensional list parameterGrid. Note that
			# emptyRow must be a copy, hence the constructor call.
			self.parameterGrid.insert( numRowBefore, list( emptyRow ) )
			
		"""
		Delete a row from the parameter grid.
		"""
		def deleteRow( self, index ):
			# Make sure the given index is valid, if not raise an exception.
			if index >= self.numRows:
				raise ScimitarSpeciesError( 'Index of row to delete is out of range!' )
				return
				
			# Delete the row from the data structure.
			del self.parameterGrid[index]
			
			# Decrement the number of rows by one.
			self.numRows -= 1
			
		"""
		Set a member element of the parameter grid identified by the row and column.
		"""
		def setElement( self, row, column, newValue ):
			self.parameterGrid[row][column] = newValue
		
		"""
		Get a member element of the parameter grid identified by the row and column.
		"""	
		def getElement( self, row, column ):
			return self.parameterGrid[row][column]
			
		"""
		Print the parameter grid to STDOUT.
		"""
		#TODO: Make this look nice!
		def printGrid( self ):
			print self.parameterGrid
			
		"""
		Check if a range value is valid.
		"""
		def isValidRange( value ):
			nums = value.split( ':' )
			for i in range( 0, 2 ):
				try:
					float( nums[i] )
				except ValueError:
					return false
			return true
			
		"""
		Check the parameter grid for any errors, and if there are any, raise an exception.
		"""
		def checkGrid( self ):
			# Check that the variable names are strings that do not start with a number
			# and do not contain backslashes, do not contain spaces.
			for i in range( 0, self.numRows ):
				element = self.getElement( i, 0 )
				if not element[0].isalpha():
					raise ScimitarGridError( "Variable name in row " + str( i ) + " must begin with a letter." )
				if not len( element.split() ) == 1:
					raise ScimitarGridError( "Variable name in row " + str( i ) + " cannot contain spaces." )
				if not len( element.split( '/' ) ) == 1:
					raise ScimitarGridError( "Variable name in row " + str( i ) + " cannot contain backslashes." )
					
			# Check that all data types are valid types.
			validDataTypes = [ "int", "real", "range", "file", "function" ]
			for i in range( 0, self.numRows ):
				element = self.getElement( i, 1 )
				if element not in validDataTypes:
					raise ScimitarGridError( "Data type '" + element + "' in row " + str( i ) + " is not a valid type." ) 
					
			# Check that the values match the data types.
			for i in range( 0, self.numRows ):
				dataType = self.getElement( i, 1 )
				value = self.getElement( i, 2 )
				if dataType.strip() == "int":
					try:
						allValues = _expandValues( value, "int" )
						for val in allValues:
							int( val )
					except ValueError:
						raise ScimitarGridError( "Value '" + value + "' in row " + str( i ) + " is not a valid int." )
				elif dataType.strip() == "real":
					try:
						allValues = _expandValues( value, "real" )
						for val in allValues:
							float( val )
					except ValueError:
						raise ScimitarGridError( "Value '" + value + "' in row " + str( i ) + " is not a valid real." )
				elif dataType.strip() == "range":
					if not _isValidRange( value ):
						raise ScimitarGridError( "Value '" + value + " in row " + str( i ) + " is not a valid range." )
				elif dataType.strip() == "file":
					pass
				elif dataType.strip() == "function":
					pass
					
			# Check that a correct directory order exists.
			directoryOrders = []
			for i in range( 0, self.numRows ):
				if not self.getElement( i, 3 ).strip() == DEFAULT_EMPTY_ELEMENT:
					directoryOrders.append( self.getElement( i, 3 ) )
			
			directoryOrders.sort()
			
			# Make sure that the first element is '1'.
			if not directoryOrders[0].strip() == '1':
				raise ScimitarGridError( "The parameter grid must contain a directory order of 1." )
				 
			# Make sure that the rest of the dir orders are consecutive.
			currentOrderToCheck = 1
			for i in range( 1, len( directoryOrders ) ):
				currentOrderToCheck += 1
				if ( not directoryOrders[i].strip() == str( currentOrderToCheck ) ) and \
				   ( not directoryOrders[i].strip() == DEFAULT_EMPTY_ELEMENT ):
					raise ScimitarGridError( "All directory orders must be consecutive." )
		
		"""
		Get a list of all the runs that will be executed.
		"""			
		def generateRunListing( self ):
			# Get list of directory orders.
			directoryOrders = []
			for i in range( 0, self.numRows ):
				if not self.getElement( i, 3 ).strip() == DEFAULT_EMPTY_ELEMENT:
					directoryOrders.append( self.getElement( i, 3 ) )
			directoryOrders.sort()
			
			# Get rows with expanded values for each directory order.
			rowsToInclude = []
			for directoryOrder in directoryOrders:
				for i in range( 0, self.numRows ):
					if self.getElement( i, 3 ) == directoryOrder:
						rowsToInclude.append( [ self.getElement( i, 0 ), _expandValues( self.getElement( i, 2 ), self.getElement( i, 1 ) ) ] )
						
			# Generate the run listing from these rows.
			runListing = []
			# Start with the first row:
			for value in rowsToInclude[0][1]:
				runListing.append( rowsToInclude[0][0] + "_" + str( value )  + "/" )
			# Remove the first row from rowsToInclude:
			del rowsToInclude[0]
			
			# Iterate over the remaining rows.
			for row in rowsToInclude:
				newRunListing = []
				for run in runListing:
					for value in row[1]:
						newRunListing.append( run + row[0] + "_" + str( value ) + "/" )
				runListing = list( newRunListing )
				
			return runListing
		
		"""
		Get a count of the number of runs.
		"""
		def getRunCount( self ):
			return len( self.generateRunListing() )