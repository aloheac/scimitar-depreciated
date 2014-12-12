####################################################################
# Scimitar
# A visual driver for computational parameter-space exploration.
#
# Main entry point for Scimitar. To run, execute ./Scimitar.py or
# python Scimitar.py. Scimitar must run with Python 2.x. Requires
# wxPython 3.0.3 or greater.
#
# Version 6.0
# 11 December 2014
#
# Joaquin E. Drut, Andrew C. Loheac
# Department of Physics and Astronomy
# University of North Carolina at Chapel Hill
####################################################################

import wx
import ScimitarCore
from ScimitarMainForm import *
from ScimitarRunForm import *

# Generate the main Scimitar GUI window.

app = wx.App()
mainScimitarForm = ScimitarMainForm()
mainScimitarForm.Show()

app.MainLoop()
