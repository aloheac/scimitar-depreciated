"""
Scimitar Style Parameter Input Parser Library
Version 0.1
24 July 2014

Andrew C. Loheac
Department of Physics and Astronomy
University of North Carolina at Chapel Hill
"""

class IncorrectInputFormat(Exception):
    """
    Exception that is raised when the specified Scimitar input file is not in
    the correct format.
    """
    def __init__(self, value):
	self.value = value

    def __str__(self):
	return repr(self.value)

class ScimitarInputParser:
    """
    Easily loads a Scimitar styled input file into a dictionary data structure
    and a list.
    """
    def __init__(self, filename=""):
	"""
	Default constructor.

	Parameters:
	  filename -- Filename of the input file to load.
	"""
        self.filename = filename;
        
    def loadParameters(self):
	"""
	Load the parameters from the specified input file into a dictionary
	where the parameter description (specified after the '#' in the input
	file) is paired with the parameter value.
	"""
        # Open the Scimitar input file.
        file = open( self.filename )

        # Initialize an empty dictionary and list to store the parameter
        # description value pairs.
	self.paramDictionary = { }
	self.paramList = [ ]

        for line in file:
	    # Split the line into the parameter value and description.
            split_line = line.split()

	    # If the line does not contain two tokens, then the input file is
            # not in the appropriate format. Raise an exception.
            if len( split_line ) != 2:
                raise IncorrectInputFormat("The specified Scimitar input file is not in the correct format.")

	    # Insert the new parameter description and value into the
            # dictionary and a list.
            self.paramDictionary[ split_line[ 1 ][1:] ] = split_line[ 0 ]
	    self.paramList.append( split_line[ 0 ] )

    def getDictionary(self):
	"""
	Returns a copy of the dictionary generated by the loadParameters()
	call.
	"""
        return self.paramDictionary

    def getList(self):
	"""
	Returns a copy of the list generated by the loadParameters() call.
	"""
	return self.paramList

    def setFilename(self, filename):
	"""
	Sets a new input filename.
	"""
	self.filename = filename