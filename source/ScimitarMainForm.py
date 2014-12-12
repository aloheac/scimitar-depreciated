####################################################################
# Scimitar: ScimitarGUI: Scimitar Main Form
#
# Main Scimitar form.
#
# Version 6.0
# 8 December 2014
#
# Joaquin E. Drut, Andrew C. Loheac
# Department of Physics and Astronomy
# University of North Carolina at Chapel Hill
####################################################################

import wx
import wx.richtext as wx_richtext
import time
import ScimitarCore
from ScimitarRunForm import *

MENU_ID_OPEN_RUN = 100
MENU_ID_NEW_RUN = 101
COLOR_RED = (255, 0, 0)

class RichLogControl( wx_richtext.RichTextCtrl ):
	def __init__( self, panel ):
		wx_richtext.RichTextCtrl.__init__( self, panel, size=(300,400), style=wx.VSCROLL|wx.HSCROLL )
	
	"""
	Write an error to the log file in the main window.
	"""
	def WriteLogError( self, err ):
		self.MoveEnd()
		self.BeginTextColour( COLOR_RED )
		self.BeginBold()
		self.WriteText( "Error: " )
		self.EndBold()
		self.WriteText( err )
		self.EndTextColour()
		self.Newline()
		self.ScrollIntoView( self.GetCaretPosition(), 0 )
		
	"""
	Write standard text to the log file in the main window.
	"""
	def WriteLogText( self, text ):
		self.MoveEnd()
		self.WriteText( text )
		self.Newline()
		self.ScrollIntoView( self.GetCaretPosition(), 0 )
	
	"""
	Write standard text to the log file in the main window.
	"""	
	def WriteLogHeader( self, text ):
		self.MoveEnd()
		self.BeginBold()
		self.WriteText( text )
		self.EndBold()
		self.Newline()
		self.ScrollIntoView( self.GetCaretPosition(), 0 )
		
	"""
	Write important information to the log file in the main window.
	"""
	def WriteLogInformation( self, text ):
		self.MoveEnd()
		self.BeginTextColour( (0, 0, 255) )
		self.BeginBold()
		self.WriteText( text )
		self.EndBold()
		self.EndTextColour()
		self.Newline()
		
		
class ScimitarMainForm( wx.Frame ):
	def __init__( self ):
		wx.Frame.__init__( self, None, -1, 'Scimitar', size=(400, 300) )
		self.InitializeUI()
		
	def InitializeUI( self ):
		# ***** MENU BAR *****.
		menuBar = wx.MenuBar()
		
		# Setup menus for the frame.
		menuFile = wx.Menu()
		menuFile_NewRun = menuFile.Append( MENU_ID_NEW_RUN, "&Create a new run" )
		menuFile_OpenRun = menuFile.Append( MENU_ID_OPEN_RUN, "&Open an existing run" )
		menuFile_Quit = menuFile.Append( wx.ID_EXIT, "&Quit" )
		menuBar.Append( menuFile, "&File" )
		
		menuHelp = wx.Menu()
		menuHelp_About = menuHelp.Append( wx.ID_ABOUT, "&About Scimitar" )
		menuBar.Append( menuHelp, "&Help" )
		
		self.SetMenuBar( menuBar )
		# ***** END OF MENU BAR *****
		
		# ***** TOOLBAR *****
		toolbar = self.CreateToolBar( wx.TB_TEXT )
		toolbarIconSize = ( 24, 24 )
		
		# Get icon images.
		newRun_bmp = wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, toolbarIconSize)
		openRun_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, toolbarIconSize)
		close_bmp = wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_OTHER, toolbarIconSize)
		help_bmp = wx.ArtProvider.GetBitmap(wx.ART_HELP, wx.ART_TOOLBAR, toolbarIconSize)
		
		toolbar_newRun = toolbar.AddLabelTool( wx.ID_ANY, "New Run", newRun_bmp, shortHelp = "Create a new run file." )
		toolbar_openRun = toolbar.AddLabelTool( wx.ID_ANY, "Open Run", openRun_bmp, shortHelp = "Open an existing run file." )
		toolbar_help = toolbar.AddLabelTool( 10, "Help", help_bmp, shortHelp = "Open the documentation for Scimitar." )
		toolbar_exit = toolbar.AddLabelTool( wx.ID_ANY, "Quit", close_bmp, shortHelp = "Quit Scimitar." )
		
		toolbar.Realize()
		# ***** END OF TOOLBAR *****
		
		# ***** EVENT BINDINGS *****
		self.Bind( wx.EVT_MENU, self.onExit, menuFile_Quit )
		
		self.Bind( wx.EVT_TOOL, self.onNewRun, toolbar_newRun )
		self.Bind( wx.EVT_TOOL, self.onOpenRun, toolbar_openRun )
		self.Bind( wx.EVT_TOOL, self.onExit, toolbar_exit )
		# ***** END OF EVENT BINDINGS *****
		
		# ***** MAIN PANEL *****
		self.mainPanel = wx.Panel( self )
		self.mainBoxSizer = wx.BoxSizer( wx.VERTICAL )
	
		self.log = RichLogControl( self.mainPanel )
		self.log.SetEditable( False )
		
		self.mainBoxSizer.Add( self.log, 1, wx.ALIGN_CENTER|wx.EXPAND )
		self.mainPanel.SetSizerAndFit( self.mainBoxSizer )
		# ***** END OF MAIN PANEL *****
		
		self.log.WriteLogHeader("Welcome to Scimitar!")
		self.log.WriteLogText("Version 6.0 alpha (Dec 2014)\n")
		self.log.WriteLogText("Need some guidance getting started?")
		self.log.WriteLogText("Click on the 'Help' button above.\n")
		self.log.WriteLogText("Date: " + time.strftime('%a %d %b %Y %H:%M:%S'))
		
	def onExit( self, evt ):
		self.Close()
		
	def onOpenRun(self, evt):
		openFileDialog = wx.FileDialog( self, "Open Scimitar Run", "", "", "Scimitar Run files (*.srn)|*.srn", wx.FD_OPEN|wx.FD_FILE_MUST_EXIST )
		if openFileDialog.ShowModal() == wx.ID_CANCEL:
			return  # A file was not opened.
		
		self.log.WriteLogText("Opening run file '" + str( openFileDialog.GetPath() ) + "'.")
		loadedRun = ScimitarCore.openRunFromFile( openFileDialog.GetPath() )
		newRunEditor = ScimitarRunForm( self, loadedRun )
		
	def onNewRun(self, evt):
		newRunEditor = ScimitarRunForm( self, ScimitarCore.ScimitarRun( ScimitarCore.ScimitarSpecies() ) )
		self.log.WriteLogText("Creating a new run.")