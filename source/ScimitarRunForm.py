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
import wx.propgrid as wx_propgrid
import ScimitarCore

class RunNotebook( wx.Notebook ):
    def __init__(self, RunForm, parent ):
        wx.Notebook.__init__(self, parent, style=wx.BK_DEFAULT, size=(500, 50) )
        
        parameterGridPanel = wx.Panel(self, -1)
        settingsPanel = wx.Panel(self, -1)
        executionPanel = wx.Panel(self, -1)
        
        self.AddPage(parameterGridPanel, "Parameter Grid")
        self.AddPage(settingsPanel, "Run Configuration")
        self.AddPage(executionPanel, "Execution Settings")

        # ***** PARAMETER GRID TAB *****
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
        
        # ***** RUN SETTINGS TAB *****
        runSettingsSizer = wx.BoxSizer( wx.VERTICAL )
        RunForm.runPropertiesGrid = wx_propgrid.PropertyGrid( settingsPanel, size=(300, 300) )
        #runSettingsSizer.Add( wx.StaticText( settingsPanel, label="This tab describes basic run configuration settings for the Scimitar script. A resource manager must also be selected and configured on the following tab." ), 1 )
        runSettingsSizer.Add( RunForm.runPropertiesGrid, 2, wx.EXPAND )
        settingsPanel.SetSizerAndFit( runSettingsSizer )
        RunForm.runPropertiesGrid.Append( wx_propgrid.PropertyCategory( "Basic Script Properties" ) )
        RunForm.runPropertiesGrid.Append( wx_propgrid.StringProperty( "Script filename", "scriptFilename", RunForm.run.runSettings.scriptFilename ) )
        RunForm.runPropertiesGrid.Append( wx_propgrid.DirProperty( "Script output location", "scriptLocation", RunForm.run.runSettings.scriptLocation ) )
        RunForm.runPropertiesGrid.Append( wx_propgrid.PropertyCategory( "Executable Properties" ) )
        RunForm.runPropertiesGrid.Append( wx_propgrid.FileProperty( "Executable filename", "executableFilename", RunForm.run.runSettings.executableFilename ) )
        RunForm.runPropertiesGrid.Append( wx_propgrid.FileProperty( "Output filename", "outputFilename", RunForm.run.runSettings.outputFilename ) )
        RunForm.runPropertiesGrid.Append( wx_propgrid.FileProperty( "Input filename", "inputFilename", RunForm.run.runSettings.inputFilename ) )
        RunForm.runPropertiesGrid.Append( wx_propgrid.DirProperty( "Source path", "sourcePath", RunForm.run.runSettings.sourcePath ) )
        RunForm.runPropertiesGrid.Append( wx_propgrid.PropertyCategory( "Basic Script Tasks" ) )
        RunForm.runPropertiesGrid.Append( wx_propgrid.BoolProperty("Compile executable from source", "optionCompileSource", RunForm.run.runSettings.optionCompileSource ) )
        RunForm.runPropertiesGrid.Append( wx_propgrid.BoolProperty("Build directory structure", "optionBuildDirectoryStructure", RunForm.run.runSettings.optionBuildDirectoryStructure ) )
        RunForm.runPropertiesGrid.Append( wx_propgrid.BoolProperty("Disable input redirection", "optionDisableInputRedirection", RunForm.run.runSettings.optionDisableInputRedirection ) )
        
        # ***** EXECUTION PANEL *****
        executionSettingsSizer = wx.BoxSizer( wx.VERTICAL )
        RunForm.singleMachinePropertyGrid = wx_propgrid.PropertyGrid( executionPanel )
        RunForm.executionChoiceBook = wx.Choicebook( executionPanel, id=wx.ID_ANY )
        executionSettingsSizer.Add( RunForm.executionChoiceBook, 1, wx.EXPAND )
        executionPanel.SetSizerAndFit( executionSettingsSizer )
        
        # SINGLE MACHINE SETTINGS
        panelSingleMachine = wx.Panel( RunForm.executionChoiceBook )
        panelPBS = wx.Panel( RunForm.executionChoiceBook )
        panelSingleMachineMPI = wx.Panel( RunForm.executionChoiceBook )
        panelPBSMPI = wx.Panel( RunForm.executionChoiceBook )
        
        RunForm. propertyGridSingleMachine = wx_propgrid.PropertyGrid( panelSingleMachine )
        sizerGridSingleMachine = wx.BoxSizer( wx.VERTICAL )
        sizerGridSingleMachine.Add( RunForm.propertyGridSingleMachine, 1, wx.EXPAND )
        panelSingleMachine.SetSizerAndFit( sizerGridSingleMachine )
        RunForm.propertyGridSingleMachine.Append( wx_propgrid.PropertyCategory( "Resources" ) )
        RunForm.propertyGridSingleMachine.Append( wx_propgrid.IntProperty( "Number of simultaneous runs", "numRuns", 62 ))
        
        RunForm.executionChoiceBook.AddPage( panelSingleMachine, "Single Machine or Interactive Job")
        RunForm.executionChoiceBook.AddPage( panelPBS, "PBS Scheduler on Cluster")
        RunForm.executionChoiceBook.AddPage( panelSingleMachineMPI, "Single Machine or Interactive Job using MPI")
        RunForm.executionChoiceBook.AddPage( panelPBSMPI, "PBS Scheduler on Cluster using MPI")
class ParameterGrid( wx_grid.Grid ):
    def __init__(self, parent ):
        wx_grid.Grid.__init__( self, parent, size=(100, 100) )
        
class ScimitarRunForm( wx.Frame ):
    def __init__(self, parent, run ):
        wx.Frame.__init__(self, parent, -1, 'Scimitar Run Editor', size=(600,500) )
        
        self.MainLog = parent.log
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
        self.Bind( wx_propgrid.EVT_PG_CHANGED, self.onUpdateRunParameterGrid, self.runPropertiesGrid )
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
        self.Bind( wx.EVT_TOOL, self.onCreateScript, toolbar_createScript )
        self.Bind( wx.EVT_TOOL, self.onSaveAsRun, toolbar_saveAs )                           
        # ***** END OF TOOLBAR *****
        
        self.mainPanel = wx.Panel( self )
        runNB = RunNotebook( self, self.mainPanel )
        self.mainBoxSizer = wx.BoxSizer( wx.HORIZONTAL )
        self.mainBoxSizer.Add( runNB, 1, wx.EXPAND )
        self.mainPanel.SetSizerAndFit( self.mainBoxSizer )
        
        self.Show()
        
    def onReportCard(self, evt):
    	self.MainLog.WriteLogHeader("\nReport Card")
        try:
        	self.run.species.checkGrid()
        except (ScimitarCore.ScimitarGridError, ScimitarCore.ScimitarRunError) as err:
        	self.MainLog.WriteLogError( err.value )
        	return
        self.MainLog.WriteLogText( self.run.getReportCard() )
        
    def onCreateScript(self, evt):
    	self.MainLog.WriteLogHeader("\nGenerate Script")
    	self.MainLog.WriteLogText("Checking parameter grid for errors...")
    	try:
    		self.run.species.checkGrid()
    	except ScimitarCore.ScimitarGridError as err:
    		self.MainLog.WriteLogError( err.value )
    		return
    	self.MainLog.WriteLogText("Parameter grid verified. Checking run settings and generating execution script...")
    	
    	try:
    		self.run.generateScript()
    	except ScimitarCore.ScimitarRunError as err:
    		self.MainLog.WriteLogError( err.value )
    		return
    	self.MainLog.WriteLogText("Done! The script is located at '" + self.run.runSettings.scriptFilename + "'.")
        
    def onSaveAsRun(self, evt):
        saveFileDialog = wx.FileDialog( self, "Save Scimitar Run", "", "", "Scimitar Run files (*.srn)|*.srn", wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT )
        if saveFileDialog.ShowModal() == wx.ID_CANCEL:
            return  # File is not to be saved.
        
        ScimitarCore.writeRunToFile(self.run, saveFileDialog.GetPath())
        self.MainLog.WriteLogText("Run file '" + str( saveFileDialog.GetPath() ) + "' saved.")
        
    def onParameterGridChanged(self, evt):
        # Save parameter grid to the run.
        for i in range( 0, self.run.species.numRows ):
            for j in range( 0, self.run.species.numColumns ):
                self.run.species.setElement( i, j, str( self.speciesGrid.GetCellValue( i, j ) ) )
                
    def onUpdateRunParameterGrid(self, evt):
        if evt.GetProperty().GetName() == "scriptFilename":
            self.run.runSettings.scriptFilename = evt.GetProperty().GetValue()
        elif evt.GetProperty().GetName() == "scriptLocation":
            self.run.runSettings.scriptLocation = evt.GetProperty().GetValue()
        elif evt.GetProperty().GetName() == "executableFilename":
            self.run.runSettings.executableFilename = evt.GetProperty().GetValue()
        elif evt.GetProperty().GetName() == "inputFilename":
            self.run.runSettings.inputFilename = evt.GetProperty().GetValue()
        elif evt.GetProperty().GetName() == "outputFilename":
            self.run.runSettings.outputFilename = evt.GetProperty().GetValue()
        elif evt.GetProperty().GetName() == "sourcePath":
            self.run.runSettings.sourcePath = evt.GetProperty().GetValue()
        elif evt.GetProperty().GetName() == "optionCompileSource":
            self.run.runSettings.optionCompileSource = evt.GetProperty().GetValue()
        elif evt.GetProperty().GetName() == "optionBuildDirectorySTructure":
            self.run.runSettings.optionBuildDirectoryStructure = evt.GetProperty().GetValue()
        elif evt.GetProperty().GetName() == "optionDisableInputRedirection":
            self.run.runSettings.optionDisableInputRedirection = evt.GetProperty().GetValue()