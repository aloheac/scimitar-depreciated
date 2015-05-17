####################################################################
# Scimitar: AnalysisCoreModules: Panels: SplitTabularData
#
# Module for splitting tabular data up into columns.
#
# Version 6.0
# 16 May 2015
#
# Joaquin E. Drut, Andrew C. Loheac
# Department of Physics and Astronomy
# University of North Carolina at Chapel Hill
####################################################################

import wx

class SplitTabularDataPanel( wx.Panel ):
    def __init__(self, parent, module):
        wx.Panel.__init__(self, parent )
        self.module = module
        
        self.mainSizer = wx.BoxSizer( wx.VERTICAL )
        
        settingsBox = wx.StaticBox( self, -1, "Module Settings" )
        settingsBoxSizer = wx.StaticBoxSizer( settingsBox, wx.VERTICAL )
        settingsBoxSizer.Add( wx.StaticText( self, label="There are no settings to adjust for this module." ) )
        
        outputBox = wx.StaticBox( self, -1, "Module Output" )
        outputBoxSizer = wx.StaticBoxSizer( outputBox, wx.VERTICAL )
        self.outputListCtrl = wx.ListCtrl( self, style=wx.LC_REPORT )
        outputBoxSizer.Add( self.outputListCtrl )
        
        numRows = len( module.output )
        numCols = 0
        for i in range( 0, numRows ):
            if len( module.output[i] ) > numCols:
                numCols = len( module.output[i] )
                
        for i in range( 0, numCols ):
            self.outputListCtrl.InsertColumn( i, "Column " + str( i ) )
            
        for i in range( 0, numRows ):
            rowToAdd = module.output[i]
            for j in range( 0, numCols - len( module.output[i] ) ):
                rowToAdd.append( "" )
                
            self.outputListCtrl.Append( rowToAdd )
            
        self.mainSizer.Add( settingsBoxSizer )
        self.mainSizer.Add( outputBoxSizer )
        self.SetSizerAndFit( self.mainSizer )