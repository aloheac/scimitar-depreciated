####################################################################
# Scimitar: ScimitarModule:CheckStatus
#
# Module that will generate a secondary script that may be run to
# print the status of the run to the console.
#
# Version 6.0
# 8 December 2014
#
# Joaquin E. Drut, Andrew C. Loheac
# Department of Physics and Astronomy
# University of North Carolina at Chapel Hill
####################################################################

from PreExecutionModule import *

class CheckStatus( PreExecutionModule ):
    def __init__( self, run ):
        PreExecutionModule.__init__( self, "Check Status Script Generator", 5, run )
        
    def getScriptContribution( self ):
        contribution = ""
        if self.run.runSettings.optionGenerateCheckStatusScript:
            contribution += "# ***** PreExecution: CheckStatus *****\n"
            contribution += "print '>> Generating script for checking status...'\n"
            contribution += "checkStatusScript = open( './checkstat.py', 'w' )\n"
            contribution += "checkStatusScript.write(\"from subprocess import Popen, PIPE\\n\")\n"
            contribution += "checkStatusScript.write(\"import sys\\n\")\n"
            contribution += "checkStatusScript.write(\"import time\\n\")\n"
            contribution += "checkStatusScript.write(\"from os.path import isfile\\n\")\n\n"
            contribution += "checkStatusScript.write(\"numlines = 5\\n\")\n"
            contribution += "checkStatusScript.write(\"jobListing = " + str( self.run.species.generateRunListing() ) + "\\n\")\n"
            contribution += "checkStatusScript.write('jobID = 0\\n')\n"
            contribution += "checkStatusScript.write('for job in jobListing:\\n')\n"
            contribution += "checkStatusScript.write('    print \">> (\" + str( jobID ) + \") \" + str( job )\\n')\n"
            contribution += "checkStatusScript.write('    if isfile( \"./exec/\" + str( job ) + \"/" + str( self.run.runSettings.outputFilename ) + "\"):\\n')\n"
            contribution += "checkStatusScript.write('        proc = Popen([\"tail\", \"-n 5\", \"./exec/\" + str( job ) + \"/" + str( self.run.runSettings.outputFilename ) + "\"], stdout=PIPE)\\n')\n"
            contribution += "checkStatusScript.write('        ( output, err ) = proc.communicate()\\n')\n"
            contribution += "checkStatusScript.write('        exitstat = proc.wait()\\n')\n"
            contribution += "checkStatusScript.write('        print output\\n')\n"
            contribution += "checkStatusScript.write('    else:\\n')\n"
            contribution += "checkStatusScript.write('        print \"Run has not yet started or the path is invalid.\"\\n')\n"
            contribution += "checkStatusScript.write('    jobID += 1\\n')\n"
            contribution += "checkStatusScript.write('    print \"-------------------------------------------------------\"\\n')\n"
            contribution += "checkStatusScript.close()\n"
            contribution += "# ***** End of PreExecution: CheckStatus *****\n"
        return contribution