####################################################################
# Scimitar: ScimitarGUI: ProgressBarDialog
#
# Displays a progress bar to a user when a time-intensive process
# is run.
#
# Version 6.0
# 18 May 2015
#
# Joaquin E. Drut, Andrew C. Loheac
# Department of Physics and Astronomy
# University of North Carolina at Chapel Hill
###################################################################

import wx
from time import sleep
import threading

class UpdateProgressBarThread( threading.Thread ):
    def __init__(self, dialog):
        threading.Thread.__init__(self)
        self.dialog = dialog
    
    def run(self):
        while not self.dialog.pipeline.eventProgress == -1:
            self.dialog.progressBar.SetValue( self.dialog.pipeline.eventProgress )
            self.dialog.Layout()
            print self.dialog.progressBar.GetValue()
            sleep( 0.1 )
        self.dialog.pipeline.eventProgress = 0
        self.dialog.Close()
        
class ProgressBarDialog( wx.Dialog ):
    def __init__( self, parent, pipeline ):
        wx.Dialog.__init__( self, parent, title="Please wait...", size=(200,100) )
        self.pipeline = pipeline
        self.parent = parent
        
        self.mainPanel = wx.Panel( self )
        self.mainSizer = wx.BoxSizer( wx.VERTICAL )
        
        self.progressLabel = wx.StaticText( self.mainPanel, label="Please wait..." )
        self.mainSizer.Add( (0, 7) )
        self.mainSizer.Add( self.progressLabel )
        self.mainSizer.Add( (0, 7) )
        
        self.progressBar = wx.Gauge( self )
        self.mainSizer.Add( self.progressBar )
        
        self.mainPanel.SetSizerAndFit( self.mainSizer )
        
        UpdateProgressBarThread( self ).start()
        
        self.Show()