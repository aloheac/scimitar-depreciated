####################################################################
# Scimitar: ScimitarGUI: AnalysisModulePickerForm
#
# Form for allowing the user to choose a module to be added to the
# analysis pipeline.
#
# Version 6.0
# 16 May 2015
#
# Joaquin E. Drut, Andrew C. Loheac
# Department of Physics and Astronomy
# University of North Carolina at Chapel Hill
###################################################################

import wx

class AnalysisModulePickerForm( wx.Dialog ):
    def __init__( self, parent ):
        wx.Dialog.__init__( self, parent, title="Analysis Module Picker", size=(400,350) )
        self.chosenModule = -1 
        self.chosenClass = -1
        
        self.mainPanel = wx.Panel( self )
        self.mainSizer = wx.BoxSizer( wx.VERTICAL )
        
        self.mainSizer.Add( (0, 7) )
        self.mainSizer.Add( wx.StaticText( self.mainPanel, label="  Add module to:" ), wx.TOP )
        self.mainSizer.Add( (0, 7) )
        
        self.moduleClassChooser = wx.ComboBox( self.mainPanel, size=(380, 25) )
        self.moduleClassChooser.Append( "Reduction" )
        self.moduleClassChooser.Append( "Active" )
        self.moduleClassChooser.Append( "Inactive" )
        self.moduleClassChooser.SetSelection( 0 )  # Initially set drop down to 'Reduction'.
        self.mainSizer.Add( self.moduleClassChooser, wx.TOP  )
        
        self.mainSizer.Add( (0, 7) )
        self.mainSizer.Add( wx.StaticText( self.mainPanel, label="  Select a module to add:" ), wx.TOP)
        self.mainSizer.Add( (0, 7) )
        
        self.moduleListBox = wx.ListBox( self.mainPanel, size=(380, 200) )
        self.mainSizer.Add( self.moduleListBox, wx.EXPAND)
        self.mainPanel.SetSizerAndFit( self.mainSizer )
        
        self.mainSizer.Add( (0, 7) )
        selectModuleButton = wx.Button( self.mainPanel, label="Select Module", size=(200, 30) )
        self.mainSizer.Add( selectModuleButton, wx.BOTTOM|wx.CENTER)
        self.mainSizer.Add( (0, 7) )
        
        self.Bind( wx.EVT_BUTTON, self.onSelectModule, selectModuleButton )
        
        self.moduleListBox.Append( "Reduction : Split Tabular Data" )
        self.moduleListBox.Append( "Formatting : Strip QMC Header" )
        self.moduleListBox.Append( "Output : Write Tabular Data to Disk" )
        self.moduleListBox.Append( "Reduction : Average Columns")
        
        self.moduleListBox.SetSelection( 0 )
        
        self.mainPanel.SetSizerAndFit( self.mainSizer )
        self.ShowModal()
        
    def onSelectModule(self, evt):
        self.chosenModule = self.moduleListBox.GetSelection()
        self.chosenClass = self.moduleClassChooser.GetSelection()
        self.Close()