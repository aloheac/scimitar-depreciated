####################################################################
# Scimitar: ScimitarGUI: Scimitar Help Browser
#
# Main Scimitar form.
#
# Version 6.0.1
# 25 March 2015
#
# Joaquin E. Drut, Andrew C. Loheac
# Department of Physics and Astronomy
# University of North Carolina at Chapel Hill
####################################################################

import wx.html2
import os.path
import sys

class ScimitarHelpBrowser( wx.Frame ):
    def __init__( self, parent ):
        wx.Frame.__init__( self, parent, title="Scimitar Help" )
        
        self.mainPanel = wx.Panel( self )
        self.boxSizer = wx.BoxSizer( wx.HORIZONTAL )
        self.helpBrowser = wx.html2.WebView.New( self.mainPanel )
        self.boxSizer.Add( self.helpBrowser, 1, wx.ALL|wx.EXPAND, border=5 )
        self.mainPanel.SetSizerAndFit( self.boxSizer )
        
        if getattr( sys, 'frozen', False ):
            basedir = sys._MEIPASS
        else:
            basedir = os.path.dirname(__file__)
        
        self.helpURL = basedir +  "/resources/ScimitarHelp.html"
        self.helpBrowser.LoadURL( "file://" + self.helpURL )
        self.helpBrowser.ClearHistory()
           
        browserToolbar = self.CreateToolBar( wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT )
        
        close_bmp = wx.Bitmap( basedir + '/resources/exit.png' )
        forward_bmp = wx.Bitmap( basedir + '/resources/forward.png' )
        back_bmp = wx.Bitmap( basedir + '/resources/back.png' )
        home_bmp = wx.Bitmap( basedir + '/resources/home.png' )
        
        self.toolbarHome = browserToolbar.AddLabelTool( wx.ID_ANY, "Home", home_bmp, shortHelp="Go home." )
        self.toolbarBack = browserToolbar.AddLabelTool( wx.ID_ANY, "Back", back_bmp, shortHelp="Go back." )
        self.toolbarForward = browserToolbar.AddLabelTool( wx.ID_ANY, "Forward", forward_bmp, shortHelp="Go forward." )
        self.toolbarClose = browserToolbar.AddLabelTool( wx.ID_ANY, "Close", close_bmp, shortHelp="Close." )
        
        self.Bind( wx.EVT_TOOL, self.onHomeButton, self.toolbarHome )
        self.Bind( wx.EVT_TOOL, self.onBackButton, self.toolbarBack )
        self.Bind( wx.EVT_TOOL, self.onForwardButton, self.toolbarForward )
        self.Bind( wx.EVT_TOOL, self.onCloseButton, self.toolbarClose )
        browserToolbar.Realize()
        
        self.SetSize( (800,600) )
        self.Show()
        
    def onHomeButton( self, evt ):
        self.helpBrowser.LoadURL( "file://" + self.helpURL )
        
    def onForwardButton( self, evt ):
        if self.helpBrowser.CanGoForward():
            self.helpBrowser.GoForward()
        
    def onBackButton(self, evt):
        if self.helpBrowser.CanGoBack():
            self.helpBrowser.GoBack()
        
    def onCloseButton(self, evt):
        self.Close()