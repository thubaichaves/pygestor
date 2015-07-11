"""
PureMVC Python Demo - wxPython Employee Admin 
By Toby de Havilland <toby.de.havilland@puremvc.org>
Copyright(c) 2007-08 Toby de Havilland, Some rights reserved.
"""

# import wx.grid
from pyGestorForms import enum
import nisk
# import nisk.widgets
import logging
from nisk import *


class WxApp:
    def __init__(self):
        self.pleno = None
        self.x = AppFrame()
        self.loop = urwid.MainLoop(self.x, unhandled_input=self.keyHandler)


    def run(self):
        # MDI.getInstance().MainHost = self
        tui.mdi = tui(mainhost=self)
        self.pleno = True
        self.loop.run()


    def stop(self):
        raise urwid.ExitMainLoop()


    def keyHandler(self, input):
        pass


    def get_Loop(self):
        return self.loop;


    def get_Frame(self):
        return self.x;


class AppFrame(urwid.Frame):
    userForm = None
    userList = None
    rolePanel = None

    def __init__(self):
        self.rolePanel = RolePanel(self)
        self.userList = UserList(self)
        self.userForm = UserForm(self)
        # cbox =urwid.BoxAdapter(self.userList,25)#
        cbox = urwid.Columns([self.userForm, self.rolePanel], dividechars=3)
        super(AppFrame, self).__init__(urwid.Filler(cbox), footer=urwid.BoxAdapter(self.userList, 25))


class RolePanel(nisk.widgets.LineBox):
    EVT_ADD_ROLE = "EVT_ADD_ROLE"

    EVT_REMOVE_ROLE = "EVT_REMOVE_ROLE"

    signals = [EVT_ADD_ROLE, EVT_REMOVE_ROLE]

    user = None
    selectedRole = None

    roleList = None
    roleCombo = None
    addBtn = None
    removeBtn = None

    def __init__(self, parent):
        self.roleList = nisk.widgets.wgtListBox([])
        self.roleList._connect_signal('onselect', self.onListClick)

        self.roleCombo = nisk.widgets.wgtComboBox()
        self.roleCombo._connect_signal('onselect', self.onComboClick)

        self.addBtn = nisk.widgets.wgtButton("Add User", self.onAdd)
        self.addBtn.Disable()

        self.cancelBtn = nisk.widgets.wgtButton("Cancel", self.onRemove)
        self.cancelBtn.Disable()

        nisk.widgets.LineBox.__init__(self, urwid.Text("teste"), id=1)
        pass

    def updateRoleList(self, items):
        self.roleList.Clear()
        self.roleList.AppendItems(items)

    def updateRoleCombo(self, choices, default):
        self.roleCombo.Clear()
        self.roleCombo.AppendItems(choices)
        self.roleCombo.SetValue(default)

    def onComboClick(self, evt):
        if not self.roleCombo.GetValue() == enum.ROLE_NONE_SELECTED:
            self.addBtn.Enable()
        else:
            self.addBtn.Disable()
        self.roleList.SetSelection(-1)
        self.selectedRole = self.roleCombo.GetValue()

    def onListClick(self, evt):
        if not self.roleList.GetSelection() == enum.ROLE_NONE_SELECTED:
            self.removeBtn.Enable()
        else:
            self.removeBtn.Disable()
        self.roleCombo.SetValue(enum.ROLE_NONE_SELECTED)
        self.selectedRole = self.roleList.GetStringSelection()

    def onAdd(self, evt):
        self._emit(EVT_ADD_ROLE, self.GetId())

    def onRemove(self, evt):
        self._emit(self, self.EVT_REMOVE_ROLE, self.GetId())


class MyDataTableColumnDef(DataTableColumnDef):
    def default_format(self, v):
        textattr = "normal"
        if not isinstance(v, tuple):
            return super(MyDataTableColumnDef, self).default_format(v)

        textattr, t = v
        text = urwid.Text((textattr, s), align=self.align)
        text.val = t
        cell = urwid.Padding(text, left=self.padding, right=self.padding)
        text.sort_key = self.sort_key
        text.sort_fn = self.sort_fn
        l = list()
        cell = urwid.AttrMap(cell, self.attr_map, self.focus_map)
        if self.sizing == None or self.sizing == "given":
            l.append(self.width)
        else:
            l += ['weight', self.width]
        l.append(cell)
        return tuple(l)


class DataTableTest(nisk.datatable.DataTable):
    columns = [
        MyDataTableColumnDef("Userna'", width=10),
        MyDataTableColumnDef("First Name", width=10),
        MyDataTableColumnDef("Last Name", width=10),
        MyDataTableColumnDef("Email", width=10),
        MyDataTableColumnDef("Department", width=10),
        MyDataTableColumnDef("Password", width=10)
    ]
    l = [
        # (1, 2.12314, "c",2, 99.9555, "q"),
        # 		{ 'foo': 6, 'bar': 4, 'baz': "a",'foox': 6, 'barx': 4, 'bazx': "a"},
        #           (2, 99.9555, "q", 2.12314, "c",2),
        #           (5, 6.9555, "b", 2.12314, "c",2),
        #           (4, 103, "a", 2.12314, "c",2)
    ]

    def query(self, **kwargs):
        for r in self.l:
            yield r

    def keypress(self, size, key):
        if key in ('<', '>'):
            self.cycle_index((key == '>') and 1 or -1)
        return super(DataTableTest, self).keypress(size, key)


class UserList(nisk.widgets.LineBox):
    EVT_USER_SELECTED = "EVT_USER_SELECTED"

    EVT_NEW = "EVT_NEW"

    EVT_DELETE = "EVT_DELETE"

    signals = [EVT_USER_SELECTED, EVT_NEW, EVT_DELETE]

    userGrid = None
    newBtn = None
    deleteBtn = None

    users = None
    selectedUser = None


    def __init__(self, parent):

        self.userGrid = DataTableTest()

        self.userGrid._connect_signal('EVT_GRID_SELECT_CELL', self.onSelect)
        self.userGrid._connect_signal('EVT_GRID_CELL_CHANGE', self.onSelect)
        self.userGrid._connect_signal('click', self.onSelect)

        self.newBtn = nisk.widgets.wgtButton("New", self.onNew)
        # self.newBtn.Disable()

        self.deleteBtn = nisk.widgets.wgtButton("Delete", self.onDelete)
        #self.deleteBtn.Disable()

        # nisk.widgets.LineBox.__init__(self,self.userGrid ,id=2)
        nisk.widgets.LineBox.__init__(self, self.userGrid, id=2)

        pass

    def updateUserGrid(self, users):
        if self.pleno:
            self.userGrid.ClearGrid()
        else:
            logging.debug('tentando limpar antes de inicio pleno')

        self.users = users
        for i in range(len(users)):
            self.userGrid.add_row([
                users[i].username,
                users[i].fname,
                users[i].lname,
                users[i].email,
                users[i].department,
                users[i].password
            ])
        # self.userGrid.SetCellValue(i, 0, users[i].username)
        # self.userGrid.SetCellValue(i, 1, users[i].fname)
        # self.userGrid.SetCellValue(i, 2, users[i].lname)
        # self.userGrid.SetCellValue(i, 3, users[i].email)
        # self.userGrid.SetCellValue(i, 4, users[i].department)
        # self.userGrid.SetCellValue(i, 5, users[i].password)
        self.userGrid.AutoSize()
        pass

    def onSelect(self, evt):
        try:
            self.selectedUser = self.users[evt.GetRow()]
            self.userGrid.SelectRow(evt.GetRow())
            self._emit(self, self.EVT_USER_SELECTED, self.GetId())
        except IndexError:
            pass

    def deSelect(self):
        self.userGrid.SelectRow(-1)

    def onNew(self, evt):
        self._emit(self, self.EVT_NEW, self.GetId())
        self.deSelect()

    def onDelete(self, evt):
        if self.selectedUser:
            self._emit(self, self.EVT_DELETE, self.GetId())
            self.deSelect()


class UserForm(nisk.widgets.LineBox):
    EVT_ADD = "EVT_ADD"
    EVT_UPDATE = "EVT_UPDATE"
    EVT_CANCEL = "EVT_CANCEL"

    signals = [EVT_ADD, EVT_CANCEL, EVT_UPDATE]

    MODE_ADD = "modeAdd";
    MODE_EDIT = "modeEdit";

    user = None
    mode = None

    usernameInput = None
    firstInput = None
    lastInput = None
    emailInput = None
    passwordInput = None
    confirmInput = None
    departmentCombo = None
    addBtn = None
    cancelBtn = None

    def __init__(self, parent):
        self.parent = parent
        self.firstInput = nisk.widgets.wgtFieldBox(caption='First Name')
        self.firstInput._connect_signal("change", self.checkValid)

        self.lastInput = nisk.widgets.wgtFieldBox(caption='Last Name')
        self.lastInput._connect_signal("change", self.checkValid)

        self.emailInput = nisk.widgets.wgtFieldBox(caption='Email')
        self.emailInput._connect_signal("change", self.checkValid)

        self.usernameInput = nisk.widgets.wgtFieldBox(caption='Username')
        self.usernameInput._connect_signal("change", self.checkValid)

        self.passwordInput = nisk.widgets.wgtFieldBox(caption='Password')
        self.passwordInput._connect_signal("change", self.checkValid)

        self.confirmInput = nisk.widgets.wgtFieldBox(caption='Confirm')
        self.confirmInput._connect_signal("change", self.checkValid)

        self.departmentCombo = nisk.widgets.wgtComboBox();

        self.addBtn = nisk.widgets.wgtButton("Add User", self.onAdd)

        self.cancelBtn = nisk.widgets.wgtButton("Cancel", self.onCancel)

        self._fields = [self.usernameInput,
                        self.firstInput,
                        self.lastInput,
                        self.emailInput,
                        self.passwordInput,
                        self.confirmInput,
                        self.departmentCombo,
                        self.addBtn,
                        self.cancelBtn]

        f = [urwid.AttrMap(field, 'InfoHeaderText')
             for field in self._fields]

        self.fields = urwid.Pile(f)

        nisk.widgets.LineBox.__init__(self, self.fields, id=3)


    def updateUser(self, user):
        self.user = user
        self.usernameInput.SetValue(self.user.username)
        self.firstInput.SetValue(self.user.fname)
        self.lastInput.SetValue(self.user.lname)
        self.emailInput.SetValue(self.user.email)
        self.passwordInput.SetValue(self.user.password)
        self.confirmInput.SetValue(self.user.password)
        self.departmentCombo.SetValue(self.user.department)
        self.checkValid()

    def updateDepartmentCombo(self, choices, default):
        self.departmentCombo.Clear()
        self.departmentCombo.AppendItems(choices)
        self.departmentCombo.SetValue(default)

    def updateMode(self, mode):
        self.mode = mode
        if self.mode == self.MODE_ADD:
            self.addBtn.SetLabel("Add User")
        else:
            self.addBtn.SetLabel("Update User")

    def onAdd(self, evt):
        if self.mode == self.MODE_ADD:
            # self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(self.EVT_ADD, self.GetId()))
            self._emit(self, self.EVT_ADD, self.GetId())
        else:
            # self.GetEventHandler().ProcessEvent(wx.PyCommandEvent(self.EVT_UPDATE, self.GetId()))
            self._emit(self, self.EVT_UPDATE, self.GetId())
        self.checkValid()

    # nisk.ShowDialog("ok")

    def onCancel(self, evt):
        self.parent.userList.userGrid.ClearGrid()
        self._emit(self, self.EVT_CANCEL, self.GetId())

    def checkValid(self, evt=None, *arg):
        if self.enableSubmit(self.usernameInput.GetValue(), self.passwordInput.GetValue(), self.confirmInput.GetValue(),
                self.departmentCombo.GetValue()):
            # self.addBtn.Enable()
            # tui.ShowDialog("ADD ENB")
            pass
        else:
            pass
            # self.addBtn.Disable()
            # tui.mdi.ShowDialog("ADD DIS")

    def enableSubmit(self, u, p, c, d):
        logging.debug('u: %s p %s c %s d %s' % (u, p, c, d))
        return (len(u) > 0 and len(p) > 0 and p == c )  #and not d == enum.DEPT_NONE_SELECTED)