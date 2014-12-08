####################################################################
# Scimitar: ScimitarSpecies
#
# Class definition for a Scimitar species.
#
# Version 6.0
# 7 December 2014
#
# Joaquin E. Drut, Andrew C. Loheac
# Department of Physics and Astronomy
# University of North Carolina at Chapel Hill
####################################################################

from Globals import *

DEFAULT_NUM_ROWS = 10
DEFAULT_NUM_COLUMNS = 4

class ScimitarGridError(Exception):
	def __init__( self, value ):
		self.value = value
		
	def __str__( self ):
		return repr( self.value )
		
class ScimitarSpecies:		
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
				emptyRow.append( '--' )
			for j in range( 0, DEFAULT_NUM_ROWS ):
				self.parameterGrid.append( list( emptyRow ) )
		
		def addRow( self, numRowBefore ):
			# Increment the row dimensions by one.
			self.numRows += 1
			
			# Generate a list that is an empty row.
			emptyRow = []
			for i in range( 1, dimensions[1] ):
				emptyRow.append( '--' )
				
			# Insert the new row into the two-dimensional list parameterGrid. Note that
			# emptyRow must be a copy, hence the constructor call.
			self.parameterGrid.insert( numRowBefore, list( emptyRow ) )
			
		def setElement( self, row, column, newValue ):
			self.parameterGrid[row][column] = newValue
			
		def getElement( self, row, column ):
			return self.parameterGrid[row][column]
			
		#TODO: Make this look nice!
		def printGrid( self ):
			print self.parameterGrid
			
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