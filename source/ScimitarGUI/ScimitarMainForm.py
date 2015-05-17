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
from os import path
import sys
import wx.richtext as wx_richtext
from time import strftime
import ScimitarCore
from ScimitarRunForm import *
from ScimitarHelpBrowser import *
from ScimitarUncertaintyFormatterForm import *
from ScimitarAnalysisForm import *

MENU_ID_OPEN_RUN = 100
MENU_ID_NEW_RUN = 101
COLOR_RED = (255, 0, 0)

"""
Main log control for the Scimitar main form.
"""
class RichLogControl( wx_richtext.RichTextCtrl ):
	def __init__( self, panel ):
		wx_richtext.RichTextCtrl.__init__( self, panel, size=(300,400), style=wx.VSCROLL|wx.HSCROLL )
	
	"""
	Write an error to the log file in the main window.
	"""
	# NOTE: KeyEvent for the down arrow is 317.
	def WriteLogError( self, err ):
		self.MoveEnd()
		self.BeginTextColour( COLOR_RED )
		self.BeginBold()
		self.WriteText( "Error: " )
		self.EndBold()
		self.WriteText( err )
		self.EndTextColour()
		self.Newline()
		self.ScrollIntoView( self.GetCaretPosition(), 317 )
		
	"""
	Write standard text to the log file in the main window.
	"""
	def WriteLogText( self, text ):
		self.MoveEnd()
		self.WriteText( text )
		self.Newline()
		self.ScrollIntoView( self.GetCaretPosition(), 317 )
			
	"""
	Write standard text to the log file in the main window.
	"""	
	def WriteLogHeader( self, text ):
		self.MoveEnd()
		self.BeginBold()
		self.WriteText( text )
		self.EndBold()
		self.Newline()
		self.ScrollIntoView( self.GetCaretPosition(), 317 )
		
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
		self.ScrollIntoView( self.GetCaretPosition(), 317 )
		
class ScimitarMainForm( wx.Frame ):
	def __init__( self ):
		wx.Frame.__init__( self, None, -1, 'Scimitar', size=(400, 300) )
		self.InitializeUI()
		
	"""
	User interface initialization routine.
	"""
	def InitializeUI( self ):
		# ***** MENU BAR *****.
		menuBar = wx.MenuBar()
		
		# Setup menus for the frame.
		menuFile = wx.Menu()
		menuFile_NewRun = menuFile.Append( MENU_ID_NEW_RUN, "&New Run" )
		menuFile_OpenRun = menuFile.Append( MENU_ID_OPEN_RUN, "&Open Run..." )
		menuFile_Quit = menuFile.Append( wx.ID_EXIT, "&Quit" )
		menuBar.Append( menuFile, "&File" )
		
		menuTools = wx.Menu()
		menuTools_UncertaintyFormatter = menuTools.Append( wx.ID_ANY, "Uncertainty Formatter" )
		menuBar.Append( menuTools, "&Tools" )
		
		menuHelp = wx.Menu()
		menuHelp_Docs = menuHelp.Append( wx.ID_ANY, "&Documentation")
		menuHelp_About = menuHelp.Append( wx.ID_ABOUT, "&About Scimitar" )
		menuBar.Append( menuHelp, "&Help" )
		
		self.SetMenuBar( menuBar )
		
		# ***** END OF MENU BAR *****
		
		# ***** TOOLBAR *****
		toolbar = self.CreateToolBar( wx.TB_TEXT )
		toolbarIconSize = ( 24, 24 )
		
		# Get icon images.
		# Identify the absolute path of the images, whether we are running the script in
		# a normal Python environment or if we are in a frozen state (running in an 
		# executable bundled by pyinstaller).
		if getattr( sys, 'frozen', False ):
			basedir = sys._MEIPASS
		else:
			basedir = path.dirname(__file__)
			
		newRun_bmp = wx.Bitmap( basedir + '/resources/new.png' ) #wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, toolbarIconSize)
		openRun_bmp = wx.Bitmap( basedir + '/resources/open.png' ) #wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, toolbarIconSize)
		close_bmp = wx.Bitmap( basedir + '/resources/exit.png' ) #wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_OTHER, toolbarIconSize)
		help_bmp = wx.Bitmap( basedir + '/resources/help.png' ) #wx.ArtProvider.GetBitmap(wx.ART_HELP, wx.ART_TOOLBAR, toolbarIconSize)
		import_bmp = wx.Bitmap( basedir + '/resources/import.png' )
		analysis_bmp = wx.Bitmap( basedir + '/resources/analysis.png' )
		
		toolbar_newRun = toolbar.AddLabelTool( wx.ID_ANY, "New Run", newRun_bmp, shortHelp = "Create a new run file." )
		toolbar_openRun = toolbar.AddLabelTool( wx.ID_ANY, "Open Run", openRun_bmp, shortHelp = "Open an existing run file." )
		toolbar_import = toolbar.AddLabelTool( wx.ID_ANY, "Import", import_bmp, shortHelp="Import a set of parameters and values from a text file.")
		toolbar_analysis = toolbar.AddLabelTool( wx.ID_ANY, "Analysis", analysis_bmp, shortHelp="Analyze data produced by a Scimitar run.")
		toolbar_help = toolbar.AddLabelTool( 10, "Help", help_bmp, shortHelp = "Open the documentation for Scimitar." )
		toolbar_exit = toolbar.AddLabelTool( wx.ID_ANY, "Quit", close_bmp, shortHelp = "Quit Scimitar." )
		
		toolbar.Realize()
		# ***** END OF TOOLBAR *****
		
		# Set window icon.
		self.SetIcon( wx.Icon( basedir + '/resources/scimitar.ico' ) )
		
		# ***** EVENT BINDINGS *****
		self.Bind( wx.EVT_MENU, self.onExit, menuFile_Quit )
		self.Bind( wx.EVT_MENU, self.onNewRun, menuFile_NewRun )
		self.Bind( wx.EVT_MENU, self.onOpenRun, menuFile_OpenRun )
		self.Bind( wx.EVT_MENU, self.onAboutBox, menuHelp_About )
		self.Bind( wx.EVT_MENU, self.onShowHelp, menuHelp_Docs )
		self.Bind( wx.EVT_MENU, self.onShowUncertaintyFormatter, menuTools_UncertaintyFormatter )
		self.Bind( wx.EVT_TOOL, self.onNewRun, toolbar_newRun )
		self.Bind( wx.EVT_TOOL, self.onOpenRun, toolbar_openRun )
		self.Bind( wx.EVT_TOOL, self.onExit, toolbar_exit )
		self.Bind( wx.EVT_TOOL, self.onImport, toolbar_import ) 
		self.Bind( wx.EVT_TOOL, self.onShowHelp, toolbar_help )
		self.Bind( wx.EVT_TOOL, self.onShowAnalysisForm, toolbar_analysis )
		# ***** END OF EVENT BINDINGS *****
		
		# ***** MAIN PANEL *****
		self.mainPanel = wx.Panel( self )
		self.mainBoxSizer = wx.BoxSizer( wx.VERTICAL )
	
		self.log = RichLogControl( self.mainPanel )
		self.log.SetEditable( False )
		
		self.mainBoxSizer.Add( self.log, 1, wx.ALIGN_CENTER|wx.EXPAND )
		self.mainPanel.SetSizerAndFit( self.mainBoxSizer )
		# ***** END OF MAIN PANEL *****
		
		# ***** ABOUT DIALOG BOX *****
		
		# ***** END ABOUT DIALOG BOX *****
		
		self.log.WriteLogHeader("Welcome to Scimitar!")
		self.log.WriteLogText("Version 6.0.2 beta (May 2015)\n")
		self.log.WriteLogText("Need some guidance getting started?")
		self.log.WriteLogText("Click on the 'Help' button above.\n")
		self.log.WriteLogText("Date: " + strftime('%a %d %b %Y %H:%M:%S'))
		
	"""
	Event Handler: Close the form upon exit.
	"""
	def onExit( self, evt ):
		self.Close()
		
	"""
	Event Handler: Launch file open dialog and open the run.
	"""
	def onOpenRun(self, evt):
		openFileDialog = wx.FileDialog( self, "Open Scimitar Run", "", "", "Scimitar Run files (*.srn)|*.srn", wx.FD_OPEN|wx.FD_FILE_MUST_EXIST )
		if openFileDialog.ShowModal() == wx.ID_CANCEL:
			return  # A file was not opened.
		
		self.log.WriteLogText("Opening run file '" + str( openFileDialog.GetPath() ) + "'.")
		loadedRun = ScimitarCore.openRunFromFile( openFileDialog.GetPath() )
		newRunEditor = ScimitarRunForm( self, loadedRun, openFileDialog.GetPath() )
		
	"""
	Event Handler: Create a new run using defaults.
	"""
	def onNewRun(self, evt):
		newRunEditor = ScimitarRunForm( self, ScimitarCore.ScimitarRun( ScimitarCore.ScimitarSpecies() ), None )
		self.log.WriteLogText("Creating a new run.")
		
	"""
	Event Handler: Create about box.
	"""
	def onAboutBox(self, evt):
		description = """A visual driver for parameter-space exploration."""
		copy = """(C) 2013 - 2015 Joaquin E. Drut, et al.
Department of Physics and Astronomy
University of North Carolina at Chapel Hill

Research supported by the U.S. National Science
Foundation under Grant No. PHY1306520 and Graduate
Research Fellowship Program under Grant No. DGE1144081."""
		
		# Get base path for Scimitar logo.
		if getattr( sys, 'frozen', False ):
			basedir = sys._MEIPASS
		else:
			basedir = path.dirname(__file__)
			
		info = wx.AboutDialogInfo()
		info.SetIcon( wx.Icon( basedir + '/resources/scimitar.png', wx.BITMAP_TYPE_PNG ) )
		info.SetName('Scimitar')
		info.SetVersion('6.0.2 beta (May 2015)')
		info.SetDescription( description )
		info.SetCopyright( copy )
		info.SetWebSite('http://user.physics.unc.edu/~drut/public_html_UNC/scimitar.html')
		info.AddDeveloper('Joaquin E. Drut')
		info.AddDeveloper('Andrew C. Loheac')
		info.AddDeveloper('Dhruv Mittal')
		info.AddDeveloper('Michael Hoffman')
		
		wx.AboutBox( info )
		
	"""
	Event Handler: Import a text file and generate the parameter grid.
	"""
	def onImport(self, evt):
		# Open dialog for user to choose file to import.
		openFileDialog = wx.FileDialog( self, "Import File", "", "", "All files (*.*)|*.*", wx.FD_OPEN|wx.FD_FILE_MUST_EXIST )
		if openFileDialog.ShowModal() == wx.ID_CANCEL:
			return  # A file was not opened.
		
		# Open the selected file and get a list of parameters and values. If the file
		# is not in a format that can be read, alert the user of an error and return.
		f_import = open( openFileDialog.GetPath(), 'r' )
		value = []
		parameter = []
		try:
			for line in f_import:
				value.append( line.split('#')[0].strip() )
				parameter.append(line.split('#')[1].strip())
		except:
			self.log.WriteLogError("The given input file is not in an acceptable format.")
			return
		f_import.close()
		
		# Generate a parameter grid and Species object from the loaded set of parameters.
		newSpecies = ScimitarCore.ScimitarSpecies()
		parameterGrid = []
		try:
			for i in range( 0, len( parameter ) ):
				parameterGrid.append([parameter[i],'--',value[i],'--'])
		except:
			self.log.WriteLogError("The given input file is not in an acceptable format.")
			return
			
		newSpecies.parameterGrid = parameterGrid
		newSpecies.numRows = len( parameter )
		
		# Show the run editor with the new species generated from the import.
		newRunEditor = ScimitarRunForm( self, ScimitarCore.ScimitarRun( newSpecies ), None )
		self.log.WriteLogText("Creating a new run from imported file.")
		
	def onShowHelp(self, evt):
		ScimitarHelpBrowser( self )
		
	def onShowUncertaintyFormatter(self, evt):
		ScimitarUncertaintyFormatterForm( self )
		
	def onShowAnalysisForm(self, evt):
		ScimitarAnalysisForm( self, None )
		