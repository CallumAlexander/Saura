# -*- coding: utf-8 -*-
# Property of Callum Alexander
# Instagram - @cal.zander
# Twitter - callum_alxndr
"""
@author: Callum
"""


#Library Imports
#-----------------------
import wx
import numpy as np
import pandas as pd
#-----------------------



#Frame Class Definition
#-----------------------
class windowClass(wx.Frame):
    
    def __init__(self, parent, title):
        super(windowClass, self).__init__(parent, title=title, size=(800,600)) #(width,height)
        
        self.Centre()
        self.Show()
#-----------------------
    
#Generate GUI
#-----------------------
app = wx.App()
windowClass(None, title='Saura Interface')
app.MainLoop()

del app
#-----------------------
#Input Datastream

#
