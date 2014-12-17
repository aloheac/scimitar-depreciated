####################################################################
# Scimitar: ScimitarGUI: Scimitar Run Form
#
# Scimitar run form.
#
# Version 6.0
# 16 December 2014
#
# Joaquin E. Drut, Andrew C. Loheac
# Department of Physics and Astronomy
# University of North Carolina at Chapel Hill
####################################################################

import wx
import wx.grid as wx_grid
import wx.propgrid as wx_propgrid
from os.path import isfile
from os import linesep
import ScimitarCore

class RunNotebook( wx.Notebook ):
    def __init__(self, RunForm, parent ):
        wx.Notebook.__init__(self, parent, style=wx.BK_DEFAULT, size=(500, 50) )
        
        # Create panels and pages for each of the three notebook tabs.
        parameterGridPanel = wx.Panel(self, -1)
        settingsPanel = wx.Panel(self, -1)
        executionPanel = wx.Panel(self, -1)
        
        self.AddPage(parameterGridPanel, "Parameter Grid")
        self.AddPage(settingsPanel, "Run Configuration")
        self.AddPage(executionPanel, "Resources and Execution")

        # ***** PARAMETER GRID TAB *****
        parameterGridSizer = wx.BoxSizer( wx.HORIZONTAL )
        RunForm.speciesGrid = ParameterGrid( parameterGridPanel )
        parameterGridSizer.Add( RunForm.speciesGrid, 1, wx.EXPAND )
        parameterGridPanel.SetSizerAndFit( parameterGridSizer )

		# Create the parameter grid control.
        RunForm.speciesGrid.CreateGrid( RunForm.run.species.numRows, RunForm.run.species.numColumns )
        RunForm.speciesGrid.SetColLabelValue( 0, "Parameter" )
        RunForm.speciesGrid.SetColLabelValue( 1, "Type")
        RunForm.speciesGrid.SetColLabelValue( 2, "Value(s)")
        RunForm.speciesGrid.SetColLabelValue( 3, "Directory Order")
        RunForm.speciesGrid.SetColSize( 3, 100 )
        
        # ***** RUN SETTINGS TAB *****
        runSettingsSizer = wx.BoxSizer( wx.VERTICAL )
        RunForm.runPropertiesGrid = wx_propgrid.PropertyGrid( settingsPanel, size=(300, 300) )
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
        RunForm.runPropertiesGrid.Append( wx_propgrid.BoolProperty("Generate status check script", "optionGenerateCheckStatusScript", RunForm.run.runSettings.optionGenerateCheckStatusScript ) )
        
        # ***** RESOURCES AND EXECUTION PANEL *****
        executionSettingsSizer = wx.BoxSizer( wx.VERTICAL )
        RunForm.singleMachinePropertyGrid = wx_propgrid.PropertyGrid( executionPanel )
        RunForm.executionChoiceBook = wx.Choicebook( executionPanel, id=wx.ID_ANY )
        executionSettingsSizer.Add( RunForm.executionChoiceBook, 1, wx.EXPAND )
        executionPanel.SetSizerAndFit( executionSettingsSizer )
        
        panelSingleMachine = wx.Panel( RunForm.executionChoiceBook )
        panelPBS = wx.Panel( RunForm.executionChoiceBook )
        panelSingleMachineMPI = wx.Panel( RunForm.executionChoiceBook )
        panelPBSMPI = wx.Panel( RunForm.executionChoiceBook )
        
        # SINGLE MACHINE SETTINGS
        RunForm.propertyGridSingleMachine = wx_propgrid.PropertyGrid( panelSingleMachine )
        sizerGridSingleMachine = wx.BoxSizer( wx.VERTICAL )
        sizerGridSingleMachine.Add( RunForm.propertyGridSingleMachine, 1, wx.EXPAND )
        panelSingleMachine.SetSizerAndFit( sizerGridSingleMachine )
        RunForm.propertyGridSingleMachine.Append( wx_propgrid.PropertyCategory( "Resources" ) )
        RunForm.propertyGridSingleMachine.Append( wx_propgrid.IntProperty( "Number of simultaneous runs", "numSimRuns", RunForm.run.availableModules.SingleMachineResourceManager.numSimRuns ) )
        RunForm.propertyGridSingleMachine.Append( wx_propgrid.IntProperty( "Process status check delay (seconds)", "procCheckWaitTime", RunForm.run.availableModules.SingleMachineResourceManager.procCheckWaitTime ) )
        RunForm.propertyGridSingleMachine.Append( wx_propgrid.PropertyCategory( "Additional Commands" ) )
        RunForm.propertyGridSingleMachine.Append( wx_propgrid.LongStringProperty( "Additional pre-execution commands", "additionalPreExecutionCommands", RunForm.run.availableModules.SingleMachineResourceManager.additionalPreExecutionCommands ) )
        RunForm.propertyGridSingleMachine.Append( wx_propgrid.LongStringProperty( "Additional post-execution commands", "additionalPostExecutionCommands", RunForm.run.availableModules.SingleMachineResourceManager.additionalPostExecutionCommands ) )
        RunForm.executionChoiceBook.AddPage( panelSingleMachine, "Single Machine or Interactive Job")
        RunForm.executionChoiceBook.AddPage( panelPBS, "PBS Scheduler on Cluster")
        #RunForm.executionChoiceBook.AddPage( panelSingleMachineMPI, "Single Machine or Interactive Job using MPI")
        #RunForm.executionChoiceBook.AddPage( panelPBSMPI, "PBS Scheduler on Cluster using MPI")
        
        # PBS SETTINGS
        RunForm.propertyGridPBS = wx_propgrid.PropertyGrid( panelPBS )
        sizerGridPBS = wx.BoxSizer( wx.VERTICAL )
        sizerGridPBS.Add( RunForm.propertyGridPBS, 1, wx.EXPAND )
        panelPBS.SetSizerAndFit( sizerGridPBS )
        RunForm.propertyGridPBS.Append( wx_propgrid.PropertyCategory( "PBS Settings" ) )
        RunForm.propertyGridPBS.Append( wx_propgrid.IntProperty( "Number of nodes", "numNodes", RunForm.run.availableModules.PBSResourceManager.numNodes ) )
        RunForm.propertyGridPBS.Append( wx_propgrid.IntProperty( "Processors per node (ppn)", "processorsPerNode", RunForm.run.availableModules.PBSResourceManager.processorsPerNode ) )
        RunForm.propertyGridPBS.Append( wx_propgrid.StringProperty( "Walltime", "walltime", RunForm.run.availableModules.PBSResourceManager.walltime ) )
        RunForm.propertyGridPBS.Append( wx_propgrid.PropertyCategory( "Additional Commands" ) )
        RunForm.propertyGridPBS.Append( wx_propgrid.LongStringProperty( "Additional pre-execution commands", "additionalPreExecutionCommands", RunForm.run.availableModules.PBSResourceManager.additionalPreExecutionCommands ) )
        RunForm.propertyGridPBS.Append( wx_propgrid.LongStringProperty( "Additional post-execution commands", "additionalPostExecutionCommands", RunForm.run.availableModules.PBSResourceManager.additionalPostExecutionCommands ) )

"""
Basic ParameterGrid that inherits from wx.grid.Grid.
"""
class ParameterGrid( wx_grid.Grid ):
    def __init__(self, parent ):
        wx_grid.Grid.__init__( self, parent, size=(100, 100) )
        
"""
Form definition for the Scimitar Run Editor.
"""
class ScimitarRunForm( wx.Frame ):
    def __init__(self, parent, run, runPath ):
        wx.Frame.__init__(self, parent, -1, 'Scimitar Run Editor', size=(600,500) )
        
        self.MainLog = parent.log
        self.run = run
        self.speciesGrid = None  # Parameter grid will be initialized upon UI initialization.
        self.runPath = runPath # Should be initialized if a run was opened from file.
        
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
        
        # Set choice of active resource manager.
        if self.run.activeResourceManager.moduleName == "Single Machine":
        	self.executionChoiceBook.SetSelection( 0 )
        elif self.run.activeResourceManager.moduleName == "PBS":
        	self.executionChoiceBook.SetSelection( 1 )
        	
        # Add remaining event bindings.
        self.Bind( wx_grid.EVT_GRID_CELL_CHANGED, self.onParameterGridChanged, self.speciesGrid )
        self.Bind( wx_propgrid.EVT_PG_CHANGED, self.onUpdateRunParameterGrid, self.runPropertiesGrid )
        self.Bind( wx_propgrid.EVT_PG_CHANGED, self.onUpdateSingleMachineParameterGrid, self.propertyGridSingleMachine )
        self.Bind( wx_propgrid.EVT_PG_CHANGED, self.onUpdatePBSParameterGrid, self.propertyGridPBS )
        self.speciesGrid.Bind( wx_grid.EVT_GRID_CELL_RIGHT_CLICK, self.onShowGridContextMenu )
        self.Bind( wx.EVT_CHOICEBOOK_PAGE_CHANGED, self.onResourceManagerSelectionChanged, self.executionChoiceBook )
        
    def InitializeUI(self, gridRows, gridColumns ):
        # ***** MENU BAR *****
        menuBar = wx.MenuBar()
        menuFile = wx.Menu()
        menuFile_Save = menuFile.Append( wx.ID_ANY, "&Save Run" )
        menuFile_SaveAs = menuFile.Append( wx.ID_ANY, "&Save Run As...")
        menuFile_UpdateModules = menuFile.Append( wx.ID_ANY, "Update Modules")
        menuBar.Append( menuFile, "&File" )
        
        self.Bind( wx.EVT_MENU, self.onSaveRun, menuFile_Save )
        self.Bind( wx.EVT_MENU, self.onSaveAsRun, menuFile_SaveAs )
        self.Bind( wx.EVT_MENU, self.onUpdateModules, menuFile_UpdateModules )
        
        self.SetMenuBar( menuBar )
        # ***** END OF MENU BAR *****
        
        # ***** TOOLBAR *****
        toolbar = self.CreateToolBar( wx.TB_TEXT )
        
        # Get icon images.
        toolbarIconSize = (21, 21)
        reportCard_bmp = wx.Bitmap('./resources/reportCard.png') #wx.ArtProvider.GetBitmap(wx.ART_REPORT_VIEW, wx.ART_TOOLBAR, toolbarIconSize)
        createScript_bmp = wx.Bitmap('./resources/createScript.png') #wx.ArtProvider.GetBitmap(wx.ART_EXECUTABLE_FILE, wx.ART_TOOLBAR, toolbarIconSize)
        save_bmp = wx.Bitmap('./resources/save.png')#wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_OTHER, toolbarIconSize)
        saveAs_bmp = wx.Bitmap('./resources/saveAs.png')#wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_OTHER, toolbarIconSize)
                                            
        toolbar_save = toolbar.AddLabelTool( wx.ID_ANY, "Save", save_bmp, shortHelp="Save the run to file." )
        toolbar_saveAs = toolbar.AddLabelTool( wx.ID_ANY, "Save As", saveAs_bmp, shortHelp="Save the run under a different filename." )
        toolbar_reportCard = toolbar.AddLabelTool( wx.ID_ANY, "Report Card", reportCard_bmp, shortHelp="Check the run configuration and parameter grid for errors." )
        toolbar_createScript = toolbar.AddLabelTool( wx.ID_ANY, "Create Script", createScript_bmp, shortHelp="Generate the Python script which will execute this run on any machine." )
        
        toolbar.Realize()  
        
        # Add toolbar event bindings.
        self.Bind( wx.EVT_TOOL, self.onReportCard, toolbar_reportCard )  
        self.Bind( wx.EVT_TOOL, self.onCreateScript, toolbar_createScript )
        self.Bind( wx.EVT_TOOL, self.onSaveAsRun, toolbar_saveAs )
        self.Bind( wx.EVT_TOOL, self.onSaveRun, toolbar_save )                           
        # ***** END OF TOOLBAR *****
        
        # Create main panel of the run editor.
        self.mainPanel = wx.Panel( self )
        runNB = RunNotebook( self, self.mainPanel )
        self.mainBoxSizer = wx.BoxSizer( wx.HORIZONTAL )
        self.mainBoxSizer.Add( runNB, 1, wx.EXPAND )
        self.mainPanel.SetSizerAndFit( self.mainBoxSizer )
        
        self.Show()
        
    """
    Event Handler: Generate report card and write output to the log of the main window.
    """
    def onReportCard(self, evt):
    	self.MainLog.WriteLogHeader("\nReport Card")
        try:
        	self.run.species.checkGrid()
        except (ScimitarCore.ScimitarGridError, ScimitarCore.ScimitarRunError) as err:
        	self.MainLog.WriteLogError( err.value )
        	return
        self.MainLog.WriteLogText( self.run.getReportCard() )
    
    """
    Event Handler: Generate script and write output to main window.
    """ 
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
    		completeScript = self.run.generateScript()
    	except ScimitarCore.ScimitarRunError as err:
    		self.MainLog.WriteLogError( err.value )
    		return
        ScimitarCore.writeScriptToFile( completeScript, self.run.runSettings.scriptLocation + '/' + self.run.runSettings.scriptFilename )
    	self.MainLog.WriteLogText("Done! The script is located at '" + self.run.runSettings.scriptFilename + "'.")
        
    """
    Event Handler: 'Save as' run.
    """
    def onSaveAsRun(self, evt):
        saveFileDialog = wx.FileDialog( self, "Save Scimitar Run", "", "", "Scimitar Run files (*.srn)|*.srn", wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT )
        if saveFileDialog.ShowModal() == wx.ID_CANCEL:
            return  # File is not to be saved.
        
        ScimitarCore.writeRunToFile(self.run, saveFileDialog.GetPath())
        self.runPath = saveFileDialog.GetPath()
        self.MainLog.WriteLogText("Run file '" + str( saveFileDialog.GetPath() ) + "' saved as.")
    
    """
    Event Handler: Save run.
    """
    def onSaveRun(self, evt):
        if self.runPath == None:
            self.onSaveAsRun( evt )
            return
        
        if isfile( self.runPath ):
            ScimitarCore.writeRunToFile( self.run, self.runPath )
            self.MainLog.WriteLogText("Run file '" + str( self.runPath ) + "' saved.")
        else:
            self.onSaveAsRun( evt )
    
    """
    Event Handler: Update ScimitarSpecies parameter grid when an entry in the parameter
    grid in the run editor is changed.
    """        
    def onParameterGridChanged(self, evt):
        # Save parameter grid to the run.
        for i in range( 0, self.run.species.numRows ):
            for j in range( 0, self.run.species.numColumns ):
                self.run.species.setElement( i, j, str( self.speciesGrid.GetCellValue( i, j ) ) )
                
    """
    Event Handler: Update ScimitarRun object when an entry in the run parameter grid is
    updated.
    """
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
        elif evt.GetProperty().GetName() == "optionGenerateCheckStatusScript":
            self.run.runSettings.optionGenerateCheckStatusScript = evt.GetProperty().GetValue()
    
    """
    Format the resulting unicode type from the PropertyGrid LongString value to 
    correctly respect new lines. The purpose of this function may seem odd, but it is
    to address an issue with respect to conversion of the unicode format that wx.propgrid
    apparently uses. The result in the ScimitarRun class should be a proper Python string.
    """
    def _fixUnicodeResult(self, value ):
    	fixedValue = ""
    	for ch in str( value ):
    		fixedValue += str( ch )
    	return fixedValue.replace( "\\n", linesep )
    	
    """
    Event Handler: Update the SingleMachineResourceManager module when an entry in the 
    respective parameter grid is updated.
    """     
    def onUpdateSingleMachineParameterGrid(self, evt):
        if evt.GetProperty().GetName() == "numSimRuns":
            self.run.availableModules.SingleMachineResourceManager.numSimRuns = evt.GetProperty().GetValue()
        elif evt.GetProperty().GetName() == "procCheckWaitTime":
            self.run.availableModules.SingleMachineResourceManager.procCheckWaitTime = evt.GetProperty().GetValue()
        elif evt.GetProperty().GetName() == "additionalPreExecutionCommands":
        	self.run.availableModules.SingleMachineResourceManager.additionalPreExecutionCommands = self._fixUnicodeResult( evt.GetProperty().GetValue() )
        elif evt.GetProperty().GetName() == "additionalPostExecutionCommands":
        	self.run.availableModules.SingleMachineResourceManager.additionalPostExecutionCommands = self._fixUnicodeResult( evt.GetProperty().GetValue() )
    
    def onUpdatePBSParameterGrid(self, evt):
    	if evt.GetProperty().GetName() == "numNodes":
    		self.run.availableModules.PBSResourceManager.numNodes = evt.GetProperty().GetValue()
    	elif evt.GetProperty().GetName() == "processorsPerNode":
    		self.run.availableModules.PBSResourceManager.processorsPerNodes = evt.GetProperty().GetValue()
    	elif evt.GetProperty().GetName() == "walltime":
    		self.run.availableModules.PBSResourceManager.walltime = evt.GetProperty().GetValue()
    	elif evt.GetProperty().GetName() == "additionalPreExecutionCommands":
        	self.run.availableModules.PBSResourceManager.additionalPreExecutionCommands = self._fixUnicodeResult( evt.GetProperty().GetValue() )
        elif evt.GetProperty().GetName() == "additionalPostExecutionCommands":
        	self.run.availableModules.PBSResourceManager.additionalPostExecutionCommands = self._fixUnicodeResult( evt.GetProperty().GetValue() )
    """
    Event Handler: Update modules of a ScimitarRun to their latest versions.
    """
    def onUpdateModules(self, evt):
        if not self.runPath == None:
            self.run = ScimitarCore.ScimitarRun( self.run.species )
            ScimitarCore.writeRunToFile( self.run, self.runPath )
            self.MainLog.WriteLogText("Scimitar modules have been updated to the latest versions for this run file and saved. Please re-open the run file.")
            self.Close()
        
    """
    Event Handler: Show the context menu that allows one to add or delete rows from the 
    parameter grid.
    """
    def onShowGridContextMenu(self, evt):
        self.contextMenu = wx.Menu()
        menuItem_AddRow = wx.MenuItem( self.contextMenu, wx.ID_ANY, "Add Row")
        menuItem_DeleteRow = wx.MenuItem( self.contextMenu, wx.ID_ANY, "Delete Row")
        self.contextMenu.AppendItem( menuItem_AddRow )
        self.contextMenu.AppendItem( menuItem_DeleteRow )
        self.Bind(wx.EVT_MENU, lambda evtAddRow: self.onAddRow( evtAddRow, evt.GetRow() ), menuItem_AddRow )
        self.Bind(wx.EVT_MENU, lambda evtDeleteRow: self.onDeleteRow( evtDeleteRow, evt.GetRow() ), menuItem_DeleteRow )
        self.PopupMenu( self.contextMenu )
        self.contextMenu.Destroy()

	"""
	Event Handler: Add a row to the parameter grid in the run form and the ScimitarSpecies
	parameter grid.
	"""
    def onAddRow( self, evtAddRow, rowNumber ):
        self.run.species.addRow( rowNumber )
        self.speciesGrid.InsertRows( rowNumber )
        for i in range( 0, self.run.species.numColumns ):
            self.speciesGrid.SetCellValue( rowNumber, i, '--' )

	"""
	Event Handler: Delete a row from the parameter grid in the run for and the
	ScimitarSpecies parameter grid.
	"""
    def onDeleteRow( self, evtDeleteRow, rowNumber ):
        self.run.species.deleteRow( rowNumber )
        self.speciesGrid.DeleteRows( rowNumber )
        
    def onResourceManagerSelectionChanged( self, evt ):
    	if evt.GetSelection() == 0:
    		self.run.activeResourceManager = self.run.availableModules.SingleMachineResourceManager
    	elif evt.GetSelection() == 1:
    		self.run.activeResourceManager = self.run.availableModules.PBSResourceManager