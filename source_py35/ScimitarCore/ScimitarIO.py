####################################################################
# Scimitar: ScimitarIO
#
# Handles standard input/output file operations for the Scimitar
# core.
#
# Version 6.0
# 8 December 2014
#
# Joaquin E. Drut, Andrew C. Loheac
# Department of Physics and Astronomy
# University of North Carolina at Chapel Hill
####################################################################

import pickle

'''
Write a given run to a binary data file using Pickle.
'''
def writeRunToFile( run, filename ):
    f = open( filename, 'wb' )
    pickle.dump( run, f, pickle.HIGHEST_PROTOCOL )
    f.close()
    
'''
Open a run file to reconstruct a ScimitarRun object.
'''
def openRunFromFile( filename ):
    f = open( filename, 'rb' )
    return pickle.load( f )
    f.close()
    
'''
Write a script to file.
'''
def writeScriptToFile( script, filename ):
    f = open( filename, 'w' )
    f.write( script )
    f.close()
    