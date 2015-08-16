"""
PureMVC Python Demo - wxPython Employee Admin 
By Toby de Havilland <toby.de.havilland@puremvc.org>
Copyright(c) 2007-08 Toby de Havilland, Some rights reserved.
"""

import wx
import wx.grid
import enum
import  wx.lib.newevent

class WxApp(wx.App):

    appFrame = None

    def OnInit(self):
        self.appFrame = AppFrame()
        #self.appFrame.Show()
        #self.SetTopWindow(self.frame)


        return True

(UpdateBarEvent, EVT_UPDATE_BARGRAPH) = wx.lib.newevent.NewEvent()
(newwin, evtnew) = wx.lib.newevent.NewEvent()
class AppFrame(wx.Frame):

    userForm = None
    userList = None
    rolePanel = None

    def __init__(self):
        wx.Frame.__init__(self,parent=None, id=-1, title="PureMVC Demo",size=(660,535))
        self.rolePanel = RolePanel(self)
        self.Bind(EVT_UPDATE_BARGRAPH, self.close)
        self.main=None

    def close(self,evt):
        self.Close()

class RolePanel(wx.Panel):

    evt_ADD_ROLE = wx.NewEventType()
    EVT_ADD_ROLE = wx.PyEventBinder(evt_ADD_ROLE, 1)

    evt_REMOVE_ROLE = wx.NewEventType()
    EVT_REMOVE_ROLE = wx.PyEventBinder(evt_REMOVE_ROLE, 2)

    user = None
    selectedRole = None

    roleList = None
    roleCombo = None
    addBtn = None
    removeBtn = None

    def __init__(self,parent):
        wx.Panel.__init__(self,parent,id=1,pos=(330,220),size=(330,300))
        #self.SetBackgroundColour('Red')

        vbox = wx.BoxSizer(wx.VERTICAL)
        hboxBottom = wx.BoxSizer(wx.HORIZONTAL)

        self.roleList = wx.ListBox(self,-1,size=(300,200))
        self.roleCombo = wx.ComboBox(self, -1, size=wx.DefaultSize)
        self.addBtn = wx.Button(self, -1, "Add")
        self.addBtn.Disable()
        self.removeBtn = wx.Button(self, -1, "Remove")
        self.removeBtn.Disable()

        hboxBottom.Add(self.roleCombo, 0, wx.RIGHT,10)
        hboxBottom.Add(self.addBtn, 0, wx.RIGHT,10)
        hboxBottom.Add(self.removeBtn, 0, wx.RIGHT,10)
        vbox.Add(self.roleList, 1, wx.TOP|wx.CENTER,10)
        vbox.Add(hboxBottom, 0, wx.TOP|wx.BOTTOM|wx.ALIGN_RIGHT,10)

        self.SetAutoLayout(True)
        self.SetSizer(vbox)
        self.Layout()
