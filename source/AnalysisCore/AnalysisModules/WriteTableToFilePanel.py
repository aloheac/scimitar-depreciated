####################################################################
# Scimitar: AnalysisCoreModules: Panels: WriteTableToFile
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

class WriteTableToFilePanel( wx.Panel ):
    def __init__(self, parent, module, pipeline ):
        wx.Panel.__init__(self, parent )
        self.module = module
        self.pipeline = pipeline
        
        self.mainSizer = wx.BoxSizer( wx.VERTICAL )
        
        self.mainSizer.Add( wx.StaticText( self, label="There are no settings to adjust for this module." ) )
        
        self.SetSizerAndFit( self.mainSizer )