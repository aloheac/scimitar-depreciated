####################################################################
# Scimitar: Basic Mathematical Expression Parser and Evaluator
#
# Provides a parser for evaluating basic mathematical expressions
# that are given as functions for a parameter in a Scimitar
# species.
#
# Version 6.0
# 28 January 2015
#
# Joaquin E. Drut, Andrew C. Loheac
# Department of Physics and Astronomy
# University of North Carolina at Chapel Hill
####################################################################

import re

"""
Object that defines a valid token type for the given grammar.
"""
class TokenType:
	def __init__( self, regex, tokenID, tokenName ):
		self.regex = re.compile( regex )  # Compiled regular expression that matches the token.
		self.tokenName = tokenName  # Short description of the token.
		self.tokenID = tokenID # Integer identifier for the token.
			
"""
Struct that contains information on an identified token.
"""
class Token:
	def __init__( self, tokenID, tokenValue ):
		self.tokenID = tokenID
		self.tokenValue = tokenValue
		
"""
Object that tokenizes a mathematical expression.
"""
class MathTokenizer:
	def __init__( self ):
		self.tokens = []
		
		self.validTokenTypes = []
		self.validTokenTypes.append( TokenType( "sin|cos|exp|ln|sqrt", 0, "FUNC" ) )
		self.validTokenTypes.append( TokenType( "\\(", 1, "OPEN_PAR" ) )
		self.validTokenTypes.append( TokenType( "\\)", 2, "CLOSE_PAR" ) )
		self.validTokenTypes.append( TokenType( "[+-]", 3, "PLUS_MINUS" ) )
		self.validTokenTypes.append( TokenType( "[*/]", 4, "MULT_DIV" ) )
		self.validTokenTypes.append( TokenType( "\\^", 5, "POWER" ) )
		self.validTokenTypes.append( TokenType( "[-+]?[0-9]*\.[0-9]+([eE][-+]?[0-9]+)?", 6, "FLOAT" ) )
		self.validTokenTypes.append( TokenType( "[-+]?[0-9]+", 7, "INT" ) )
		self.validTokenTypes.append( TokenType( "[a-zA-Z][a-zA-Z0-9]*", 8, "VARIABLE" ) )
			
	"""
	Tokenize a given string.
	"""
	def tokenize( self, str ):
		str = str.strip()
		self.tokens = []
		
		while not str == "":
			tokenMatched = False
			for tokenType in self.validTokenTypes:
				matchResult = tokenType.regex.match( str ) 
				if not matchResult == None:
					self.tokens.append( Token( tokenType.tokenID, matchResult.group() ) )
					str = str[ matchResult.end():].strip()
					tokenMatched = True
					break
					
			if not tokenMatched:
				print("'" + str.split()[0] + "' is an invalid token.")
				break
		
	"""
	Print a list of tokens and their type to STDOUT.
	"""	
	def printTokens( self ):
		i = 0
		for token in self.tokens:
			print(str( i ) + "  " + str( token.tokenID ) + "  " + token.tokenValue)
			i += 1		