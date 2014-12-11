####################################################################
# Scimitar: ScimitarGUI: Scimitar Run Form
#
# Scimitar run form.
#
# Version 6.0
# 11 December 2014
#
# Joaquin E. Drut, Andrew C. Loheac
# Department of Physics and Astronomy
# University of North Carolina at Chapel Hill
####################################################################

import wx
import wx.grid as wx_grid

class RunNotebook( wx.Notebook ):
    def __init__(self, parent ):
        wx.Notebook.__init__(self, parent, style=wx.BK_DEFAULT, size=(500, 50) )
        
        parameterGridPanel = wx.Panel(self, -1)
        settingsPanel = wx.Panel(self, -1)
        
        parameterGridSizer = wx.BoxSizer( wx.HORIZONTAL )
        speciesGrid = ParameterGrid( parameterGridPanel )
        parameterGridSizer.Add( speciesGrid, 1, wx.EXPAND )
        parameterGridPanel.SetSizerAndFit( parameterGridSizer )

        speciesGrid.CreateGrid( 10, 5 )
        speciesGrid.SetColLabelValue( 0, "Parameter" )
        speciesGrid.SetColLabelValue( 1, "Type")
        speciesGrid.SetColLabelValue( 2, "Value(s)")
        speciesGrid.SetColLabelValue( 3, "Directory Order")
        speciesGrid.SetColSize( 3, 100 )
        speciesGrid.SetColLabelValue( 4, "Notes")
        speciesGrid.SetColSize( 4, 200 )
        
        
        self.AddPage(parameterGridPanel, "Parameter Grid")
        self.AddPage(settingsPanel, "Run Configuration")
        
class ParameterGrid( wx_grid.Grid ):
    def __init__(self, parent ):
        wx_grid.Grid.__init__( self, parent, size=(100, 100) )
        
class ScimitarRunForm( wx.Frame ):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, 'Scimitar Run Editor', size=(600,500) )
        self.InitializeUI()
        
    def InitializeUI(self):
        
        # ***** TOOLBAR *****
        toolbar = self.CreateToolBar( wx.TB_TEXT )
        
        # Get icon images.
        toolbarIconSize = (21, 21)
        reportCard_bmp = wx.ArtProvider.GetBitmap(wx.ART_REPORT_VIEW, wx.ART_TOOLBAR, toolbarIconSize)
        createScript_bmp = wx.ArtProvider.GetBitmap(wx.ART_EXECUTABLE_FILE, wx.ART_TOOLBAR, toolbarIconSize)
        close_bmp = wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_OTHER, toolbarIconSize)
        save_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_OTHER, toolbarIconSize)
        saveAs_bmp = wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_OTHER, toolbarIconSize)
        help_bmp = wx.ArtProvider.GetBitmap(wx.ART_HELP, wx.ART_TOOLBAR, toolbarIconSize)
                                            
        toolbar_save = toolbar.AddLabelTool( wx.ID_ANY, "Save", save_bmp, shortHelp="Save the run to file." )
        toolbar_saveAs = toolbar.AddLabelTool( wx.ID_ANY, "Save As", saveAs_bmp, shortHelp="Save the run under a different filename." )
        toolbar_saveAs = toolbar.AddLabelTool( wx.ID_ANY, "Report Card", reportCard_bmp, shortHelp="Check the run configuration and parameter grid for errors." )
        toolbar_saveAs = toolbar.AddLabelTool( wx.ID_ANY, "Create Script", createScript_bmp, shortHelp="Generate the Python script which will execute this run on any machine." )
        
        toolbar.Realize()                                    
        # ***** END OF TOOLBAR *****
        
        self.mainPanel = wx.Panel( self )
        runNB = RunNotebook( self.mainPanel )
        self.mainBoxSizer = wx.BoxSizer( wx.HORIZONTAL )
        self.mainBoxSizer.Add( runNB, 1, wx.EXPAND )
        self.mainPanel.SetSizerAndFit( self.mainBoxSizer )
        self.Show()