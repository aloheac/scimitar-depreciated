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
import wx.lib.agw.aui as aui
import wx.propgrid as wx_propgrid
import sys
from os import path
import AnalysisCore

from AnalysisModulePickerForm import *

class ScimitarAnalysisForm( wx.Frame ):
    def __init__( self, parent ):
        wx.Frame.__init__( self, parent, title="Scimitar Data Analysis", size=(800, 600) )
        
        # Set log on the main Scimitar form.
        self.MainLog = parent.log
        
        # Set analysis pipeline associated with this form.
        self.pipeline = AnalysisCore.AnalysisPipeline()
        
        # Set up AUI manager.
        self._mgr = aui.AuiManager()
        self._mgr.SetManagedWindow( self )
         
        # Set up toolbar.
        if getattr( sys, 'frozen', False ):
            basedir = sys._MEIPASS
        else:
            basedir = path.dirname(__file__)
            
        newAnalysis_bmp = wx.Bitmap( basedir + '/resources/new.png' )
        openAnalysis_bmp = wx.Bitmap( basedir + '/resources/open.png' )
        save_bmp = wx.Bitmap( basedir + '/resources/save.png')
        saveAs_bmp = wx.Bitmap( basedir + '/resources/saveAs.png')
        up_bmp = wx.Bitmap( basedir + '/resources/up.png')
        down_bmp = wx.Bitmap( basedir + '/resources/down.png')
        add_bmp = wx.Bitmap( basedir + '/resources/add.png')
        remove_bmp = wx.Bitmap( basedir + '/resources/remove.png')
        reportCard_bmp = wx.Bitmap( basedir + '/resources/reportCard.png' )
        execute_bmp = wx.Bitmap( basedir + '/resources/createScript.png' )
        
        self.toolbar = wx.ToolBar( self, -1, wx.DefaultPosition, wx.DefaultSize, wx.TB_FLAT|wx.TB_NODIVIDER|wx.TB_TEXT )
        self.toolbar.SetToolBitmapSize(wx.Size(32,32))
        self.toolbar.AddLabelTool( wx.ID_ANY, "New", newAnalysis_bmp )
        self.toolbar.AddLabelTool( wx.ID_ANY, "Open", openAnalysis_bmp)
        self.toolbar.AddLabelTool( wx.ID_ANY, "Save", save_bmp)
        self.toolbar.AddLabelTool( wx.ID_ANY, "Save As", saveAs_bmp)
        self.toolbar.AddSeparator()
        toolAddModule = self.toolbar.AddLabelTool( wx.ID_ANY, "Add", add_bmp)
        toolRemoveModule = self.toolbar.AddLabelTool( wx.ID_ANY, "Remove", remove_bmp)
        toolMoveModuleUp = self.toolbar.AddLabelTool( wx.ID_ANY, "Up", up_bmp)
        toolMoveModuleDown = self.toolbar.AddLabelTool( wx.ID_ANY, "Down", down_bmp)
        self.toolbar.AddSeparator()
        self.toolbar.AddLabelTool( wx.ID_ANY, "Report Card", reportCard_bmp)
        self.toolbar.AddLabelTool( wx.ID_ANY, "Execute", execute_bmp)
        
        self.toolbar.Realize()
        
        self._mgr.AddPane( self.toolbar, aui.AuiPaneInfo().ToolbarPane().Top())
        
        # Set up module tree.
        self.moduleTreeCtrl = wx.TreeCtrl( self, size=(150, 200) )
        self.nodeRoot = self.moduleTreeCtrl.AddRoot( "Pipeline" )
        self.nodeSettings = self.moduleTreeCtrl.AppendItem( self.nodeRoot, 'Settings' )
        self.nodeLoadData = self.moduleTreeCtrl.AppendItem( self.nodeRoot, 'Load Data' )
        self.nodeReductionModules = self.moduleTreeCtrl.AppendItem( self.nodeRoot, 'Initial Reduction' )
        self.nodeActiveModules = self.moduleTreeCtrl.AppendItem( self.nodeRoot, 'Active' )
        self.nodeInactiveModules = self.moduleTreeCtrl.AppendItem( self.nodeRoot, 'Inactive' )
        
        self.moduleTreeCtrl.ExpandAll()
        self.moduleTreeCtrl.SelectItem( self.nodeSettings )
        
        # Setup the AUI notebook for the main pane.
        self.mainNotebook = aui.AuiNotebook( self )
        self.mainSettingsTab = TabMainSettings( self.mainNotebook, self.pipeline )
        self.loadDataTab = TabLoadData( self.mainNotebook, self.pipeline, self )
        self.mainNotebook.AddPage( self.mainSettingsTab, "Main Settings" )
        self.mainNotebook.AddPage( self.loadDataTab, "Load Data" )
        
        # Add bindings.
        self.Bind( wx.EVT_TREE_ITEM_ACTIVATED, self.onTreeItemDoubleClicked, self.moduleTreeCtrl )
        self.Bind( wx.EVT_TOOL, self.onAddNewModule, toolAddModule )
        self.Bind( wx.EVT_TOOL, self.onRemoveModule, toolRemoveModule )
        self.Bind( wx.EVT_TOOL, self.onMoveModuleUp, toolMoveModuleUp )
        self.Bind( wx.EVT_TOOL, self.onMoveModuleDown, toolMoveModuleDown )
        
        self._mgr.AddPane( self.moduleTreeCtrl, aui.AuiPaneInfo().Left().Caption("Analysis Modules") )
        self._mgr.AddPane( self.mainNotebook, aui.AuiPaneInfo().CenterPane().Caption("Module Configuration") )
        self._mgr.Update()
        
        self.moduleTreeCtrl.ExpandAll()
        self.moduleTreeCtrl.SelectItem( self.nodeSettings )
        self.Show()
        
    def onTreeItemDoubleClicked( self, evt ):
        if self.moduleTreeCtrl.GetFocusedItem() == self.nodeSettings:
            self.mainSettingsTab = TabMainSettings( self.mainNotebook, self.pipeline )
            self.mainNotebook.AddPage( self.mainSettingsTab, "Main Settings" )
        elif self.moduleTreeCtrl.GetFocusedItem() == self.nodeLoadData:
            self.loadDataTab = TabLoadData( self.mainNotebook, self.pipeline, self )
            self.mainNotebook.AddPage( self.loadDataTab, "Load Data" )
            
    def onAddNewModule(self, evt):
        self.pipeline._moduleID += 1
        picker = AnalysisModulePickerForm( self )
        treeID = None
        newModule = None
        
        if picker.chosenModule == 0:
            newModule = AnalysisCore.AnalysisModules.SplitTabularDataModule()
        if picker.chosenModule == 1:
            newModule = AnalysisCore.AnalysisModules.StripQMCHeaderModule()
            
        newModule.moduleID = self.pipeline._moduleID
        
        if picker.chosenClass == 0: # Reduction
            self.pipeline.addReductionModule( newModule )
            treeID = self.moduleTreeCtrl.AppendItem( self.nodeReductionModules, newModule.moduleName )
            self.moduleTreeCtrl.SetPyData( treeID,  self.pipeline._moduleID )
        elif picker.chosenClass == 1: # Active
            self.pipeline.addActiveModule( newModule )
            treeID = self.moduleTreeCtrl.AppendItem( self.nodeActiveModules, newModule.moduleName)
            self.moduleTreeCtrl.SetPyData( treeID,  self.pipeline._moduleID )
        elif picker.chosenClass == 2: # Inactive
            self.pipeline.addInactiveModule( newModule )
            treeID = self.moduleTreeCtrl.AppendItem( self.nodeInactiveModules, newModule.moduleName )
            self.moduleTreeCtrl.SetPyData( treeID,  self.pipeline._moduleID )
        
    def onRemoveModule(self, evt):
        if (self.moduleTreeCtrl.GetFocusedItem() == self.nodeRoot) or (self.moduleTreeCtrl.GetFocusedItem() == self.nodeReductionModules) or (self.moduleTreeCtrl.GetFocusedItem() == self.nodeActiveModules) or (self.moduleTreeCtrl.GetFocusedItem() == self.nodeInactiveModules) or (self.moduleTreeCtrl.GetFocusedItem() == self.nodeLoadData) or (self.moduleTreeCtrl.GetFocusedItem() == self.nodeSettings):
            return
        
        currentTreeItemID = self.moduleTreeCtrl.GetPyData( self.moduleTreeCtrl.GetFocusedItem() )
        self.moduleTreeCtrl.Delete( self.moduleTreeCtrl.GetFocusedItem() )
        
        for j in range(0, len( self.pipeline.reductionModules ) ):
            if self.pipeline.reductionModules[j].moduleID == currentTreeItemID:
                        del self.pipeline.reductionModules[j]
                        return
        
        for j in range(0, len( self.pipeline.activeModules ) ):
            if self.pipeline.activeModules[j].moduleID == currentTreeItemID:
                        del self.pipeline.activeModules[j]
                        return
                    
        for j in range(0, len( self.pipeline.inactiveModules ) ):
            if self.pipeline.inactiveModules[j].moduleID == currentTreeItemID:
                        del self.pipeline.inactiveModules[j]
                        return
                    
    def onMoveModuleUp(self, evt):
        if (self.moduleTreeCtrl.GetFocusedItem() == self.nodeRoot) or (self.moduleTreeCtrl.GetFocusedItem() == self.nodeReductionModules) or (self.moduleTreeCtrl.GetFocusedItem() == self.nodeActiveModules) or (self.moduleTreeCtrl.GetFocusedItem() == self.nodeInactiveModules) or (self.moduleTreeCtrl.GetFocusedItem() == self.nodeLoadData) or (self.moduleTreeCtrl.GetFocusedItem() == self.nodeSettings):
            return
        print self.pipeline.reductionModules
        currentTreeItemID = self.moduleTreeCtrl.GetPyData( self.moduleTreeCtrl.GetFocusedItem() ) 
        
        for j in range(0, len( self.pipeline.reductionModules ) ):
            if self.pipeline.reductionModules[j].moduleID == currentTreeItemID:
                        if j == 0:
                            return
                        else:
                            self.pipeline.reductionModules[j-1], self.pipeline.reductionModules[j] = self.pipeline.reductionModules[j], self.pipeline.reductionModules[j-1]
                            self.moduleTreeCtrl.DeleteChildren( self.nodeReductionModules )
                            for i in range(0, len( self.pipeline.reductionModules ) ):
                                treeID = self.moduleTreeCtrl.AppendItem( self.nodeReductionModules, self.pipeline.reductionModules[i].moduleName )
                                self.moduleTreeCtrl.SetPyData( treeID, self.pipeline.reductionModules[i].moduleID )
                            return
                        
        for j in range(0, len( self.pipeline.activeModules ) ):
            if self.pipeline.activeModules[j].moduleID == currentTreeItemID:
                        if j == 0:
                            return
                        else:
                            self.pipeline.activeModules[j-1], self.pipeline.activeModules[j] = self.pipeline.activeModules[j], self.pipeline.activeModules[j-1]
                            for i in range(0, len( self.pipeline.activeModules ) ):
                                treeID = self.moduleTreeCtrl.AppendItem( self.nodeActiveModules, self.pipeline.activeModules[i].moduleName )
                                self.moduleTreeCtrl.SetPyData( treeID, self.pipeline.activeModules[i].moduleID )
                            return
                        
        for j in range(0, len( self.pipeline.inactiveModules ) ):
            if self.pipeline.inactiveModules[j].moduleID == currentTreeItemID:
                        if j == 0:
                            return
                        else:
                            self.pipeline.inactiveModules[j-1], self.pipeline.inactiveModules[j] = self.pipeline.inactiveModules[j], self.pipeline.inactiveModules[j-1]
                            for i in range(0, len( self.pipeline.inactiveModules ) ):
                                treeID = self.moduleTreeCtrl.AppendItem( self.nodeInactiveModules, self.pipeline.inactiveModules[i].moduleName )
                                self.moduleTreeCtrl.SetPyData( treeID, self.pipeline.inactiveModules[i].moduleID )
                            return
     
    def onMoveModuleDown(self, evt):
        if (self.moduleTreeCtrl.GetFocusedItem() == self.nodeRoot) or (self.moduleTreeCtrl.GetFocusedItem() == self.nodeReductionModules) or (self.moduleTreeCtrl.GetFocusedItem() == self.nodeActiveModules) or (self.moduleTreeCtrl.GetFocusedItem() == self.nodeInactiveModules) or (self.moduleTreeCtrl.GetFocusedItem() == self.nodeLoadData) or (self.moduleTreeCtrl.GetFocusedItem() == self.nodeSettings):
            return
        print self.pipeline.reductionModules
        currentTreeItemID = self.moduleTreeCtrl.GetPyData( self.moduleTreeCtrl.GetFocusedItem() ) 
        
        for j in range(0, len( self.pipeline.reductionModules ) ):
            if self.pipeline.reductionModules[j].moduleID == currentTreeItemID:
                        if j == len( self.pipeline.reductionModules ) - 1:
                            return
                        else:
                            self.pipeline.reductionModules[j+1], self.pipeline.reductionModules[j] = self.pipeline.reductionModules[j], self.pipeline.reductionModules[j+1]
                            self.moduleTreeCtrl.DeleteChildren( self.nodeReductionModules )
                            for i in range(0, len( self.pipeline.reductionModules ) ):
                                treeID = self.moduleTreeCtrl.AppendItem( self.nodeReductionModules, self.pipeline.reductionModules[i].moduleName )
                                self.moduleTreeCtrl.SetPyData( treeID, self.pipeline.reductionModules[i].moduleID )
                            return
                        
        for j in range(0, len( self.pipeline.activeModules ) ):
            if self.pipeline.activeModules[j].moduleID == currentTreeItemID:
                        if j == len( self.pipeline.activeModules ) - 1:
                            return
                        else:
                            self.pipeline.activeModules[j+1], self.pipeline.activeModules[j] = self.pipeline.activeModules[j], self.pipeline.activeModules[j+1]
                            for i in range(0, len( self.pipeline.activeModules ) ):
                                treeID = self.moduleTreeCtrl.AppendItem( self.nodeActiveModules, self.pipeline.activeModules[i].moduleName )
                                self.moduleTreeCtrl.SetPyData( treeID, self.pipeline.activeModules[i].moduleID )
                            return
                        
        for j in range(0, len( self.pipeline.inactiveModules ) ):
            if self.pipeline.inactiveModules[j].moduleID == currentTreeItemID:
                        if j == len( self.pipeline.inactiveModules ) - 1:
                            return
                        else:
                            self.pipeline.inactiveModules[j+1], self.pipeline.inactiveModules[j] = self.pipeline.inactiveModules[j], self.pipeline.inactiveModules[j+1]
                            for i in range(0, len( self.pipeline.inactiveModules ) ):
                                treeID = self.moduleTreeCtrl.AppendItem( self.nodeInactiveModules, self.pipeline.inactiveModules[i].moduleName )
                                self.moduleTreeCtrl.SetPyData( treeID, self.pipeline.inactiveModules[i].moduleID )
                            return  
                                
class TabMainSettings( wx.Panel ):
    def __init__( self, parent, pipeline ):
        wx.Panel.__init__( self, parent=parent, id=wx.ID_ANY )
        self.pipeline = pipeline 
        
        # Setup main settings panel.
        settingsGridSizer = wx.BoxSizer( wx.HORIZONTAL )
        self.settingsGrid = wx_propgrid.PropertyGrid( self, size=(300,300) )
        settingsGridSizer.Add( self.settingsGrid, 1, wx.EXPAND )
        self.SetSizerAndFit( settingsGridSizer )
        
        self.settingsGrid.Append( wx_propgrid.PropertyCategory( "Basic Analysis Settings" ) )
        self.settingsGrid.Append( wx_propgrid.StringProperty( "Pipeline name", "pipelineName", self.pipeline.pipelineName ) )
        self.settingsGrid.Append( wx_propgrid.DirProperty( "Data directory", "dataDirectory", self.pipeline.dataDirectory ) )
        self.settingsGrid.Append( wx_propgrid.StringProperty( "Data filename", "dataFilename", self.pipeline.dataFilename ) )
        
        self.Bind( wx_propgrid.EVT_PG_CHANGED, self.onUpdateMainSettingsGrid, self.settingsGrid )
        
    def onUpdateMainSettingsGrid(self, evt):
        if evt.GetProperty().GetName() == "pipelineName":
            self.pipeline.pipelineName = evt.GetProperty().GetValue()
        elif evt.GetProperty().GetName() == "dataDirectory":
            self.pipeline.dataDirectory = evt.GetProperty().GetValue()
        elif evt.GetProperty().GetName() == "dataFilename":
            self.pipeline.dataFilename = evt.GetProperty().GetValue()
                
class TabLoadData( wx.Panel ):
    def __init__( self, parent, pipeline, form ):
        wx.Panel.__init__( self, parent=parent, id=wx.ID_ANY )
        self.pipeline = pipeline
        self.form = form
        
        allControlsSizer = wx.BoxSizer( wx.VERTICAL )
        loadControlsSizer = wx.BoxSizer( wx.HORIZONTAL )
        
        # *** LOAD CONTROLS SIZER ***
        # 'Load Data' button.
        loadControlsSizer.Add( (7, 0) )
        buttonLoadData = wx.Button( self, label="Load Data" )
        loadControlsSizer.Add( buttonLoadData, 1 )
        loadControlsSizer.Add( (7, 0) )
        
        # Run selection combo box.
        self.runSelectionCboBox = wx.ComboBox( self )
        loadControlsSizer.Add( self.runSelectionCboBox, 3, wx.EXPAND )
        
        allControlsSizer.Add( (0, 7) )
        allControlsSizer.Add( loadControlsSizer )
        allControlsSizer.Add( (0, 7) )
        
        self.dataDisplayBox = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_READONLY )
        self.dataDisplayBox.SetFont( wx.Font( 10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas' ) )
        allControlsSizer.Add( self.dataDisplayBox, 1, wx.EXPAND )
        
        self.SetSizerAndFit( allControlsSizer )
        
        self.Bind(wx.EVT_BUTTON, self.onLoadData, buttonLoadData )
        self.Bind(wx.EVT_COMBOBOX, self.onRunSelected, self.runSelectionCboBox )
        
    def onLoadData(self, evt):
        try:
            self.form.MainLog.WriteLogHeader( 'Data Analysis' )
            self.form.MainLog.WriteLogText( 'Loading data from file...' )
            self.pipeline.loadRawData()
        except AnalysisCore.AnalysisPipelineError as err:
            self.form.MainLog.WriteLogError( err.value )
        
        self.runSelectionCboBox.Clear()
        for i in range( 0, self.pipeline.numberOfRuns() ):
            self.runSelectionCboBox.Append( "(" + str( i ) + ") " + self.pipeline.getRunPath( i ) )
            
    def onRunSelected(self, evt):
        self.dataDisplayBox.SetValue( self.pipeline.rawData[ self.runSelectionCboBox.GetSelection() ] )
        