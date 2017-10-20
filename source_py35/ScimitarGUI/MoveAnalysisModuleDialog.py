####################################################################
# Scimitar: ScimitarGUI: MoveAnalysisModuleDialog
#
# Dialog for allowing the user to choose where an analysis module
# should be moved to (reduction, active, inactive).
#
# Version 6.0
# 16 May 2015
#
# Joaquin E. Drut, Andrew C. Loheac
# Department of Physics and Astronomy
# University of North Carolina at Chapel Hill
###################################################################

import wx

class MoveAnalysisModuleDialog( wx.Dialog ):
    def __init__( self, parent ):
        wx.Dialog.__init__( self, parent, title="Move Analysis Module", size=(170,120) )
        self.chosenLocation = -1 
        
        self.mainPanel = wx.Panel( self )
        self.mainSizer = wx.BoxSizer( wx.VERTICAL )
        
        self.mainSizer.Add( (0, 7) )
        self.mainSizer.Add( wx.StaticText( self.mainPanel, label="Move module to:" ), wx.TOP )
        self.mainSizer.Add( (0, 7) )
        
        self.moduleClassChooser = wx.Choice( self.mainPanel )
        self.moduleClassChooser.Append( "Reduction" )
        self.moduleClassChooser.Append( "Active" )
        self.moduleClassChooser.Append( "Inactive" )
        self.mainSizer.Add( self.moduleClassChooser, wx.EXPAND|wx.LEFT )
        self.moduleClassChooser.SetSelection( 0 )
        
        self.mainSizer.Add( (0, 7) )    
        selectLocationButton = wx.Button( self.mainPanel, label="OK" )
        self.mainSizer.Add( selectLocationButton, wx.ALIGN_CENTER_HORIZONTAL|wx.BOTTOM )
        self.mainSizer.Add( (0, 7) )
        
        self.mainPanel.SetSizerAndFit( self.mainSizer )
        
        self.Bind( wx.EVT_BUTTON, self.onSelectModule, selectLocationButton )
        
        self.ShowModal()
        
    def onSelectModule(self, evt):
        self.chosenLocation = self.moduleClassChooser.GetSelection()
        self.Close()