####################################################################
# Scimitar: ScimitarGUI: Scimitar Run Form
#
# Scimitar run form.
#
# Version 6.0
# 16 December 2014
#
# Joaquin E. Drut, Andrew C. Loheac, Dhruv K. Mittal
# Department of Physics and Astronomy
# University of North Carolina at Chapel Hill
####################################################################

import wx
import sys
import wx.grid as wx_grid
import wx.propgrid as wx_propgrid
from os.path import isfile, dirname
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
        RunForm.speciesGrid = ParameterGrid( parameterGridPanel, RunForm.run )
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
        RunForm.runPropertiesGrid.Append( wx_propgrid.LongStringProperty( "Run notes", "runNotes", RunForm.run.runNotes ) )
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
        
        RunForm.executionChoiceBook.AddPage( panelSingleMachine, "Single Machine or Interactive Job (Recovery Enabled)")
        RunForm.executionChoiceBook.AddPage( panelPBS, "PBS Scheduler on Cluster")
        #RunForm.executionChoiceBook.AddPage( panelSingleMachineMPI, "Single Machine or Interactive Job using MPI")
        #RunForm.executionChoiceBook.AddPage( panelPBSMPI, "PBS Scheduler on Cluster using MPI")
        
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
    def __init__(self, parent, run ):
        wx_grid.Grid.__init__( self, parent, size=(100, 100) )
        self.Bind(wx_grid.EVT_GRID_LABEL_RIGHT_CLICK, self.OnLabelRightClick)
        self.run = run  # Get reference to the run from the current ScimitarRunForm object.
    
    """
    Event Handler: Display the context menu when a row label is right-clicked.
    """
    def OnLabelRightClick(self, event):
        if event.GetRow() < 0:
            event.Skip
        else:
            # Define Menu Options for Label Right Click on Row 1+ 
            menu = wx.Menu()
            menuNewRow = menu.Append(wx.NewId(), "&Insert Row")
            menuDeleteRow = menu.Append(wx.NewId(), "&Delete Row(s)")
            menuCopyRow = menu.Append(wx.NewId(), "&Copy Row(s)")
            menuPasteRow = menu.Append(wx.NewId(), "&Paste Row(s)")
            menuClearRow = menu.Append(wx.NewId(), "&Clear Row(s)")

            # Bind Menu options to functions
            self.Bind(wx.EVT_MENU, lambda evt: self.onAddRow(evt, event.GetRow()), menuNewRow)
            self.Bind(wx.EVT_MENU, lambda evt: self.onDeleteRow(evt, event.GetRow()), menuDeleteRow)
            self.Bind(wx.EVT_MENU, lambda evt: self.onCopyRow(evt, event.GetRow()), menuCopyRow)
            self.Bind(wx.EVT_MENU, lambda evt: self.onPasteRow(evt, event.GetRow()), menuPasteRow)
            self.Bind(wx.EVT_MENU, lambda evt: self.onClearRow(evt, event.GetRow()), menuClearRow)

            self.PopupMenu(menu, event.GetPosition())
            menu.Destroy()

    """
    Event Handler: Add a row to the parameter grid in the run form and the ScimitarSpecies
    parameter grid.
    """
    def onAddRow( self, evtAddRow, rowNumber ):
        self.run.species.addRow( rowNumber )
        self.InsertRows( rowNumber )
        for i in range( 0, self.run.species.numColumns ):
            self.SetCellValue( rowNumber, i, '--' )

    """
    Event Handler: Delete a row from the parameter grid in the run for and the
    ScimitarSpecies parameter grid.
    """
    def onDeleteRow(self, event, rowNumber):
        selection = self.GetSelectedRows()
        if selection:
            for row in reversed(selection):
                self.DeleteRows(row)
                self.run.species.deleteRow( row )
        else:
            self.DeleteRows(rowNumber)
            self.run.species.deleteRow( rowNumber )

    """
    Event Handler: Copy a row from the parameter grid in the run into the
    clipboard.
    """
    def onCopyRow(self, event, rowNumber):
        clipdata = wx.TextDataObject()
        clipValueString = ""
        selection = self.GetSelectedRows()
        if selection:
            for row in selection:
                col = 0
                while col < self.GetNumberCols():
                    clipValueString += self.GetCellValue(row, col) + "\t"
                    col += 1
                clipValueString += "\r"
        else:
            col = 0
            while col < self.GetNumberCols():
                clipValueString += self.GetCellValue(rowNumber, col) + "\t"
                col += 1
        clipdata.SetText(clipValueString)
        wx.TheClipboard.Open()
        wx.TheClipboard.SetData(clipdata)
        wx.TheClipboard.Close()

    """
    Event Handler: Paste a row from the clipboard into the parameter grid.
    """
    def onPasteRow(self, event, rowNumber):
        if not wx.TheClipboard.IsOpened():
            wx.TheClipboard.Open()
            clipValueString = wx.TextDataObject()
            success = wx.TheClipboard.GetData(clipValueString)
            wx.TheClipboard.Close()
            if success:
                stringrows = clipValueString.GetText().split('\r')
                for row in stringrows:
                    if row == '':
                        break
                    stringItems = row.split('\t')
                    col = 0
                    while col <  self.GetNumberCols():
                        self.SetCellValue(rowNumber, col, stringItems[col])
                        self.run.species.setElement(rowNumber, col, stringItems[col])
                        col += 1
                    rowNumber += 1

    """
    Event Handler: Clear a row (replace all row elements with the default empty
    string.
    """
    def onClearRow(self, event, rowNumber):
        selection = self.GetSelectedRows()
        if selection:
            for row in selection:
                self.resetRow(row)
        else:
            self.resetRow(rowNumber)

    # General function to reset a single row to "--"
    def resetRow(self, rowNumber):
       for i in range(self.GetNumberCols()):
           self.SetCellValue(rowNumber, i, "--")
           self.run.species.setElement(rowNumber, i, "--")


"""
Form definition for the Scimitar Run Editor.
"""
class ScimitarRunForm( wx.Frame ):
    def __init__(self, parent, run, runPath ):
        wx.Frame.__init__(self, parent, -1, 'Scimitar Run Editor', size=(600,500) )
        
        self.parent = parent
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
        self.Bind( wx.EVT_CHOICEBOOK_PAGE_CHANGED, self.onResourceManagerSelectionChanged, self.executionChoiceBook )
        
    def InitializeUI(self, gridRows, gridColumns ):
        # ***** MENU BAR *****
        menuBar = wx.MenuBar()
        menuFile = wx.Menu()
        menuFile_Save = menuFile.Append( wx.ID_ANY, "&Save Run" )
        menuFile_SaveAs = menuFile.Append( wx.ID_ANY, "&Save Run As...")
        menuFile_UpdateModules = menuFile.Append( wx.ID_ANY, "Update Modules")
        menuBar.Append( menuFile, "&File" )

        menuGrid = wx.Menu()
        menuGrid_Import = menuGrid.Append(wx.ID_ANY, "&Import")
        menuGrid_Size = menuGrid.Append( wx.ID_ANY, "&Set Grid Size")
        menuGrid_Clear = menuGrid.Append( wx.ID_ANY, "&Clear Grid") 
        menuBar.Append(menuGrid, "&Grid") 
        
        self.Bind( wx.EVT_MENU, self.onSaveRun, menuFile_Save )
        self.Bind( wx.EVT_MENU, self.onSaveAsRun, menuFile_SaveAs )
        self.Bind( wx.EVT_MENU, self.onUpdateModules, menuFile_UpdateModules )

        self.Bind( wx.EVT_MENU, self.onImport, menuGrid_Import)
        self.Bind( wx.EVT_MENU, self.onSize, menuGrid_Size)
        self.Bind( wx.EVT_MENU, self.onClear, menuGrid_Clear)
        
        self.SetMenuBar( menuBar )
        # ***** END OF MENU BAR *****
        
        # ***** TOOLBAR *****
        toolbar = self.CreateToolBar( wx.TB_TEXT )
        
        # Get icon images.
        # Get the base directory depending on whether we are running in a normal Python
        # environment or in a pyinstaller package.
        if getattr( sys, 'frozen', False ):
        	basedir = sys._MEIPASS
        else:
        	basedir = dirname(__file__)
        	
        toolbarIconSize = (21, 21)
        reportCard_bmp = wx.Bitmap( basedir + '/resources/reportCard.png') #wx.ArtProvider.GetBitmap(wx.ART_REPORT_VIEW, wx.ART_TOOLBAR, toolbarIconSize)
        createScript_bmp = wx.Bitmap( basedir + '/resources/createScript.png') #wx.ArtProvider.GetBitmap(wx.ART_EXECUTABLE_FILE, wx.ART_TOOLBAR, toolbarIconSize)
        save_bmp = wx.Bitmap( basedir + '/resources/save.png')#wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_OTHER, toolbarIconSize)
        saveAs_bmp = wx.Bitmap( basedir + '/resources/saveAs.png')#wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_OTHER, toolbarIconSize)
                                            
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
        elif evt.GetProperty().GetName() == "runNotes":
        	self.run.runNotes = evt.GetProperty().GetValue()
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
    		self.run.availableModules.PBSResourceManager.processorsPerNode = evt.GetProperty().GetValue()
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
			# Save old main run settings.
			oldScriptFilename = self.run.runSettings.scriptFilename
			oldScriptLocation = self.run.runSettings.scriptLocation
			oldExecutableFilename = self.run.runSettings.executableFilename
			oldInputFilename = self.run.runSettings.inputFilename
			oldSourcePath = self.run.runSettings.sourcePath
			oldOptionCompileSource = self.run.runSettings.optionCompileSource
			oldOptionBuildDirectoryStructure = self.run.runSettings.optionBuildDirectoryStructure
			oldOptionDisableInputRedirection = self.run.runSettings.optionDisableInputRedirection
			oldOptionGenerateCheckStatusScript = self.run.runSettings.optionGenerateCheckStatusScript

			# Instantiate new run with the same species.
			self.run = ScimitarCore.ScimitarRun( self.run.species )

			# Restore old main run settings.
			self.run.runSettings.scriptFilename = oldScriptFilename
			self.run.runSettings.scriptLocation = oldScriptLocation
			self.run.runSettings.executableFilename = oldExecutableFilename 
			self.run.runSettings.inputFilename = oldInputFilename
			self.run.runSettings.sourcePath = oldSourcePath 
			self.run.runSettings.optionCompileSource = oldOptionCompileSource
			self.run.runSettings.optionBuildDirectoryStructure = oldOptionBuildDirectoryStructure
			self.run.runSettings.optionDisableInputRedirection = oldOptionDisableInputRedirection
			self.run.runSettings.optionGenerateCheckStatusScript = oldOptionGenerateCheckStatusScript

			# Save run file.
			ScimitarCore.writeRunToFile( self.run, self.runPath )
			self.MainLog.WriteLogInformation("Scimitar modules have been updated to the latest versions for this run file and saved. Modules have been reset to their defaults. Please re-open the run file.")
			self.Close()
        else:
        	self.MainLog.WriteLogInformation("This is a new run file. All modules are already the latest versions.")
      
    """
    Event Handler: Update the active resource manager when the selection is changed.
    """
    def onResourceManagerSelectionChanged( self, evt ):
    	if evt.GetSelection() == 0:
    		self.run.activeResourceManager = self.run.availableModules.SingleMachineResourceManager
    	elif evt.GetSelection() == 1:
    		self.run.activeResourceManager = self.run.availableModules.PBSResourceManager

    # Event Handler for import in grid menu:
    # Leverages existing import functionality in ScimitarForm.py
    # Destroy RunForm window -> call Import event handler

    def onImport(self, evt):
        self.Destroy()
        self.parent.onImport(None) 

    # Event Handler for resize grid in grid menu
    # Adds/Removes rows at the bottom of the grid as needed 
    def onSize(self, evt):
        message = "Specify the new number of rows in the grid:"
        current_size = str(self.speciesGrid.GetNumberRows())
        dlg = wx.TextEntryDialog(self, message, defaultValue=current_size)
        dlg.ShowModal()
        new_row_size = dlg.GetValue()
        dlg.Destroy()
        
        i_current = int(current_size)
        i_new = int(new_row_size)

        if i_new > i_current:
            self.speciesGrid.AppendRows(i_new - i_current, True)
            for i in range(i_current, i_new):
                self.run.species.addRow(i-1)
            for i in range(i_current, i_new):
                self.speciesGrid.resetRow(i)
        elif i_new < i_current:
            self.speciesGrid.DeleteRows(i_new, i_current - i_new, True)
            for i in range(i_current, i_new, -1):
                self.run.species.deleteRow(i-1)
            

    # Event Handler for clear grid in grid menu
    # Resets all cells to "--" 
    def onClear(self, evt):
        for i in range( 0, self.speciesGrid.GetNumberRows() ):
            self.speciesGrid.resetRow(i)

