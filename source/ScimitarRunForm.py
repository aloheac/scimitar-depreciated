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
import ScimitarCore

class RunNotebook( wx.Notebook ):
    def __init__(self, RunForm, parent ):
        wx.Notebook.__init__(self, parent, style=wx.BK_DEFAULT, size=(500, 50) )
        
        parameterGridPanel = wx.Panel(self, -1)
        settingsPanel = wx.Panel(self, -1)
        
        parameterGridSizer = wx.BoxSizer( wx.HORIZONTAL )
        RunForm.speciesGrid = ParameterGrid( parameterGridPanel )
        parameterGridSizer.Add( RunForm.speciesGrid, 1, wx.EXPAND )
        parameterGridPanel.SetSizerAndFit( parameterGridSizer )

        RunForm.speciesGrid.CreateGrid( RunForm.run.species.numRows, RunForm.run.species.numColumns )
        RunForm.speciesGrid.SetColLabelValue( 0, "Parameter" )
        RunForm.speciesGrid.SetColLabelValue( 1, "Type")
        RunForm.speciesGrid.SetColLabelValue( 2, "Value(s)")
        RunForm.speciesGrid.SetColLabelValue( 3, "Directory Order")
        RunForm.speciesGrid.SetColSize( 3, 100 )
        
        self.AddPage(parameterGridPanel, "Parameter Grid")
        self.AddPage(settingsPanel, "Run Configuration")
        
class ParameterGrid( wx_grid.Grid ):
    def __init__(self, parent ):
        wx_grid.Grid.__init__( self, parent, size=(100, 100) )
        
class ScimitarRunForm( wx.Frame ):
    def __init__(self, parent, run ):
        wx.Frame.__init__(self, parent, -1, 'Scimitar Run Editor', size=(600,500) )
        
        self.run = run
        self.speciesGrid = None  # Parameter grid will be initialized upon UI initialization.
        
        # Initialize modules.
        self.moduleHeaderModule = ScimitarCore.ScimitarModules.HeaderModule( run )
        self.moduleCreateDirectoryStructure = ScimitarCore.ScimitarModules.CreateDirectoryStructure( run )
        self.moduleSingleMachineResourceManager = ScimitarCore.ScimitarModules.SingleMachineResourceManager( run )
        self.moduleCompileSource = ScimitarCore.ScimitarModules.CompileSource( run )
        
        self.InitializeUI( run.species.numRows, run.species.numColumns )
        
        # Load parameter grid from the run.
        for i in range( 0, run.species.numRows ):
            for j in range( 0, run.species.numColumns ):
                self.speciesGrid.SetCellValue( i, j, self.run.species.getElement( i, j ) )
        
        # Add remaining event bindings.
        self.Bind( wx_grid.EVT_GRID_CELL_CHANGED, self.onParameterGridChanged, self.speciesGrid )
        
    def InitializeUI(self, gridRows, gridColumns ):
        
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
        toolbar_reportCard = toolbar.AddLabelTool( wx.ID_ANY, "Report Card", reportCard_bmp, shortHelp="Check the run configuration and parameter grid for errors." )
        toolbar_createScript = toolbar.AddLabelTool( wx.ID_ANY, "Create Script", createScript_bmp, shortHelp="Generate the Python script which will execute this run on any machine." )
        
        toolbar.Realize()  
        
        # Add toolbar event bindings.
        self.Bind( wx.EVT_TOOL, self.onReportCard, toolbar_reportCard )  
        self.Bind( wx.EVT_TOOL, self.onSaveAsRun, toolbar_saveAs )                           
        # ***** END OF TOOLBAR *****
        
        self.mainPanel = wx.Panel( self )
        runNB = RunNotebook( self, self.mainPanel )
        self.mainBoxSizer = wx.BoxSizer( wx.HORIZONTAL )
        self.mainBoxSizer.Add( runNB, 1, wx.EXPAND )
        self.mainPanel.SetSizerAndFit( self.mainBoxSizer )
        
        self.Show()
        
    def onReportCard(self, evt):
        self.run.species.printGrid()
        
    def onSaveAsRun(self, evt):
        saveFileDialog = wx.FileDialog( self, "Save Scimitar Run", "", "", "Scimitar Run files (*.srn)|*.srn", wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT )
        if saveFileDialog.ShowModal() == wx.ID_CANCEL:
            return  # File is not to be saved.
        
        ScimitarCore.writeRunToFile(self.run, saveFileDialog.GetPath())
    def onParameterGridChanged(self, evt):
        # Save parameter grid to the run.
        for i in range( 0, self.run.species.numRows ):
            for j in range( 0, self.run.species.numColumns ):
                self.run.species.setElement( i, j, str( self.speciesGrid.GetCellValue( i, j ) ) )