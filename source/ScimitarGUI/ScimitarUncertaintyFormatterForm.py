####################################################################
# Scimitar: ScimitarGUI: Uncertainty Formatter Form
#
# Form for formatting values and uncertainties in the format A.B(C).
#
# Version 6.0
# 5 May 2015
#
# Joaquin E. Drut, Andrew C. Loheac
# Department of Physics and Astronomy
# University of North Carolina at Chapel Hill
###################################################################

import wx
import sys
from os import path

"""
Formats a measurement given a value and its uncertainty.
  value : (float) Value of the measurement.
  err   : (float) Uncertainty of the measurement.

The value is formatted in the form A.B(C).
"""
def formatUncertainties( value, err ):
    formattedValue = ""
    if err < 1.0:
        digitsOfCertainty = 1
        uncertainty = ""
        charNo = 0
        formattedError = str( "{:f}".format( err ) ).split(".")[1]
        for char in formattedError:  # Format the error such that it is fixed floating point, not in scientific notation.
                if char == "0":
                        digitsOfCertainty += 1
                else:
                        uncertainty = str( int( round( float( str(char) + str(formattedError[charNo + 1] ) ) / 10 ) ) )
                        break
                charNo += 1
        formattingString = "{:." + str( digitsOfCertainty ) + "f}"
        formattedValue = formattingString.format( value ) + "(" + uncertainty + ")"
    else:  # err >= 1.0
        uncertainty = int( round( float( err ) ) )
        lengthOfUncertainty = len( str( uncertainty ) )
        uncertainty = int( float( uncertainty ) * 10**( -lengthOfUncertainty + 1 ) ) * 10**( lengthOfUncertainty - 1 )
        sigFigs = int( float( value ) * 10**( -lengthOfUncertainty + 1 ) )
        zerosToAdd = ""
        for i in range(0, lengthOfUncertainty - 1):
            zerosToAdd += '0'
            
        formattedValue = str( sigFigs ) + zerosToAdd + '(' + str( uncertainty ) + ')'
    return formattedValue

"""
Class definition for the Uncertainty Formatter form.
"""
class ScimitarUncertaintyFormatterForm( wx.Frame ):
    def __init__(self, parent):
        wx.Frame.__init__( self, parent, title="Uncertainty Formatter" )
        
        if getattr( sys, 'frozen', False ):
            basedir = sys._MEIPASS
        else:
            basedir = path.dirname(__file__)
            
        self.SetIcon( wx.Icon( basedir + '/resources/scimitar.ico' ) )
        
        self.mainPanel = wx.Panel( self )
        self.mainSizer = wx.GridBagSizer(3, 3)
        
        self.mainSizer.Add( wx.StaticText( self.mainPanel, label=" Values:" ), (0, 0), flag=wx.TOP|wx.EXPAND, border=5 )
        self.mainSizer.Add( wx.StaticText( self.mainPanel, label=" Uncertainties:" ), (0, 1), flag=wx.TOP|wx.EXPAND, border=5 )
        self.mainSizer.Add( wx.StaticText( self.mainPanel, label=" Formatted Data:" ), (0, 2), flag=wx.TOP|wx.EXPAND, border=5 )
        
        self.textValues = wx.TextCtrl( self.mainPanel, style=wx.TE_MULTILINE, size=(60,100) )
        self.textUncertainties = wx.TextCtrl( self.mainPanel, style=wx.TE_MULTILINE, size=(60,100) )
        self.textFormatted = wx.TextCtrl( self.mainPanel, style=wx.TE_MULTILINE|wx.TE_READONLY, size=(60,100) )
        
        self.mainSizer.Add( self.textValues, (1, 0), flag=wx.EXPAND, border=5 )
        self.mainSizer.Add( self.textUncertainties, (1, 1), flag=wx.EXPAND, border=5 )
        self.mainSizer.Add( self.textFormatted, (1, 2), flag=wx.EXPAND, border=5 )
        
        self.buttonFormat = wx.Button( self.mainPanel, wx.ID_ANY, "Format" )
        self.mainSizer.Add( self.buttonFormat, (2, 1), flag=wx.BOTTOM|wx.EXPAND, border=5 )
        self.Bind( wx.EVT_BUTTON, self.onFormat )
        
        self.mainSizer.AddGrowableCol(0)
        self.mainSizer.AddGrowableCol(1)
        self.mainSizer.AddGrowableCol(2)
        self.mainSizer.AddGrowableRow(1)
        self.mainPanel.SetSizerAndFit( self.mainSizer )
        self.Show()
    
    """
    Event handler for 'Format' button. Causes the values and uncertainties to be
    formatted and entered into the 'Formatted Values' text control.
    """
    def onFormat(self, evt):
        if not self.textValues.GetNumberOfLines() == self.textUncertainties.GetNumberOfLines():
            msgErr = wx.MessageDialog( self, "The number of values given must match the number of uncertanties given.", caption="Error", style=wx.OK|wx.ICON_ERROR )
            msgErr.ShowModal()
            return
        
        values = []
        uncertainties = []
        for line in range( 0, self.textValues.GetNumberOfLines() ):
            # Process value.
            try:
                values.append( float( self.textValues.GetLineText( line ) ) )
            except ValueError: # If a value entered cannot be casted to a float, throw an exception.
                msgErr = wx.MessageDialog( self, "Non-numerical value given in line " + str( line ) + " in the entered values.", caption="Error", style=wx.OK|wx.ICON_ERROR )
                msgErr.ShowModal()
                
            # Process uncertainty.
            try: 
                uncertainties.append( float( self.textUncertainties.GetLineText( line ) ) )
            except ValueError:
                msgErr = wx.MessageDialog( self, "Non-numerical value given in line " + str( line ) + " in the entered uncertainties.", caption="Error", style=wx.OK|wx.ICON_ERROR )
                msgErr.ShowModal()
            
        # Enter the formatted values into the 'Formatted Values' text control.
        formattedValues = ""
        for i in range(0, len( values ) ):
            formattedValues += formatUncertainties( values[i], uncertainties[i] ) + "\n"
            
        self.textFormatted.SetValue( formattedValues )