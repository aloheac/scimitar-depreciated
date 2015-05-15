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
import sys
from os import path

class ScimitarAnalysisForm( wx.Frame ):
    def __init__( self, parent ):
        wx.Frame.__init__( self, parent, title="Scimitar Data Analysis", size=(600, 400) )
        
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
        
        self.toolbar = wx.ToolBar( self, -1, wx.DefaultPosition, wx.DefaultSize, wx.TB_FLAT|wx.TB_NODIVIDER )
        self.toolbar.SetToolBitmapSize(wx.Size(32,32))
        self.toolbar.AddLabelTool( wx.ID_ANY, "New", newAnalysis_bmp )
        self.toolbar.AddLabelTool( wx.ID_ANY, "Open", openAnalysis_bmp)
        self.toolbar.AddLabelTool( wx.ID_ANY, "Save", save_bmp)
        self.toolbar.AddLabelTool( wx.ID_ANY, "Save As", saveAs_bmp)
        self.toolbar.AddSeparator()
        self.toolbar.AddLabelTool( wx.ID_ANY, "Add", add_bmp)
        self.toolbar.AddLabelTool( wx.ID_ANY, "Remove", remove_bmp)
        self.toolbar.AddLabelTool( wx.ID_ANY, "Up", up_bmp)
        self.toolbar.AddLabelTool( wx.ID_ANY, "Down", down_bmp)
        self.toolbar.AddSeparator()
        self.toolbar.AddLabelTool( wx.ID_ANY, "Report Card", reportCard_bmp)
        self.toolbar.AddLabelTool( wx.ID_ANY, "Execute", execute_bmp)
        
        self.toolbar.Realize()
        
        self._mgr.AddPane( self.toolbar, aui.AuiPaneInfo().ToolbarPane().Top())
        # Set up module tree.
        self.moduleTreeCtrl = wx.TreeCtrl( self, size=(150, 200) )
        nodeRoot= self.moduleTreeCtrl.AddRoot( "Pipeline" )
        nodeSettings = self.moduleTreeCtrl.AppendItem( nodeRoot, 'Settings')
        nodeActiveModules = self.moduleTreeCtrl.AppendItem( nodeRoot, 'Active')
        nodeInactiveModules = self.moduleTreeCtrl.AppendItem( nodeRoot, 'Inactive')
        self.mainSettingsPanel = wx.Panel( self )
        
        # Add the panes to the window manager.
        self._mgr.AddPane( self.moduleTreeCtrl, aui.AuiPaneInfo().Left().Caption("Analysis Modules") )
        self._mgr.AddPane( self.mainSettingsPanel, aui.AuiPaneInfo().CenterPane().Caption("Module Configuration") )
        self._mgr.Update()
        self.Show()