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
#
# THIS SOFTWARE IS DISTRIBUTED WITH NO WARRANTY. IT IS PROVIDED 
# "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF 
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, AND ANY
# WARRANTY THAT THIS SOFTWARE IS FREE FROM BUGS OR DEFEFCTS.
#
# IN NO EVENT, UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN
# WRITING, SHALL THE AUTHORS, OR ANY PERSON BE LIABLE FOR ANY LOSS,
# EXPENSE OR DAMAGE, OF ANY TYPE OR NATURE ARISING OUT OF THE USE
# OF, OR INABILITY TO USE THIS SOFTWARE, INCLUDING BUT NOT LIMITED
# TO LOSS OF DATA OR DATA BEING RENDERED INACCURATE.
# 
####################################################################

import wx
import ScimitarGUI

# Generate the main Scimitar GUI window.
app = wx.App()
mainScimitarForm = ScimitarGUI.ScimitarMainForm()
mainScimitarForm.Show()

app.MainLoop()