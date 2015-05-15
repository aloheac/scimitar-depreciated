####################################################################
# Scimitar: ScimitarGUI: Scimitar Analysis Form
#
# Form for data analysis of a Scimitar run.
#
# Version 6.0
# 14 May 2015
#
# Joaquin E. Drut, Andrew C. Loheac
# Department of Physics and Astronomy
# University of North Carolina at Chapel Hill
####################################################################

import wx

class ScimitarAnalysisForm( wx.Frame ):
    def __init__( self, parent ):
        wx.Frame.__init__( self, parent, title="Scimitar Data Analysis" )
        
        self.Show()