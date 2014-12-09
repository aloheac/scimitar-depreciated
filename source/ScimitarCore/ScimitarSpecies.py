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

from Globals import *

DEFAULT_NUM_ROWS = 10
DEFAULT_NUM_COLUMNS = 4
DEFAULT_EMPTY_ELEMENT = '--'

"""
Standard exception that will be raised by ScimitarGrid if an error is detected in
checkGrid().
"""
class ScimitarGridError(Exception):
	def __init__( self, value ):
		self.value = value
		
	def __str__( self ):
		return repr( self.value )

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
		
		"""
		Add a blank row to the parameter grid of the species.
		"""
		def addRow( self, numRowBefore ):
			# Increment the row dimensions by one.
			self.numRows += 1
			
			# Generate a list that is an empty row.
			emptyRow = []
			for i in range( 1, dimensions[1] ):
				emptyRow.append( str( DEFAULT_EMPTY_ELEMENT ) )
				
			# Insert the new row into the two-dimensional list parameterGrid. Note that
			# emptyRow must be a copy, hence the constructor call.
			self.parameterGrid.insert( numRowBefore, list( emptyRow ) )
			
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
				if dataType == "int":
					try:
						int( value )
					except ValueError:
						raise ScimitarGridError( "Value '" + value + "' in row " + int( i ) + " is not a valid int." )
				elif dataType == "real":
					try:
						float( value )
					except ValueError:
						raise ScimitarGridError( "Value '" + value + "' in row " + int( i ) + " is not a valid real." )
				elif dataType == "range":
					if not isValidRange( value ):
						raise ScimitarGridError( "Value '" + value + " in row " + int( i ) + " is not a valid range." )
				elif dataType == "file":
					pass
				elif dataType == "function":
					pass