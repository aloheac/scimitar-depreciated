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
Write a set of scripts to file.
'''
def writeScriptToFile( scripts, filename ):
    if len( scripts ) == 1:  # We are only writing one script. Use provided filename as is.
        f = open( filename, 'w' )
        f.write( scripts[0] )
        f.close()
    else:
        for i in range( 0, len( scripts ) ):
            # Generate filename with script number appended.
            splitFilename = filename.rsplit(".", 1)
            nextFilename = filename + "_" + str( i )  # Default for any unconventional filenames.
            if len( splitFilename ) == 2:
                nextFilename = splitFilename[0] + "_" + str( i ) + "." + splitFilename[1]

            f = open( nextFilename, 'w' )
            f.write( scripts[i] )
            f.close()
    