#!/usr/bin/python
# -*- coding: utf-8 -*-

import urwid
import nisk
import conf
import nisk.TUI
import nisk.widgets
import pyGestorModel.proxies
import nisk.dialogs
import thread, threading
from nisk import util
import logging


class frmLoginA(nisk.TUI.nestedwidget):
    def __init__(self, _widgetpai):
        self.edtUser = nisk.widgets.wgtFieldBoxDb(ltabela='sysus', tabela='lists_a', caption=u'Usuário',
                                                  params={"canedit": False})
        self.edtPass = urwid.Edit(caption = 'Senha',mask='*')
        nisk.TUI.nestedwidget.__init__(self, pai=_widgetpai, filhos=[self.edtUser, self.edtPass])
        self._constroi()

    def _constroi(self):
        _frame = urwid.SolidFill()
        _blank = urwid.Divider()
        self._lw = urwid.SimpleListWalker([
            # _blank,
            self.edtUser,
            # _blank,
            self.edtPass,
            # _blank
        ])
        _listbox = urwid.ListBox(self._lw)
        _linebox = nisk.widgets.LineBox(_listbox, title='|** Neon Gestor - Login **|')
        _linebox_ = urwid.AttrWrap(_linebox, 'field', 'field_of')

        self.widget = urwid.Overlay(_linebox_, _frame,
                                    'center', 40,
                                    'middle', 12)

    def _widgetonshow(self):
        nisk.TUI.nestedwidget._widgetonshow(self)

        self._widgetprocessa(conf.cmds.dlg_statusbar_put,
                             "Informe seu código de Usuário e Senha")

    def _widgetonunshow(self):
        nisk.TUI.nestedwidget._widgetonunshow(self)

        self._widgetprocessa(conf.cmds.dlg_statusbar_pop)

    def act_CheckLogin(self):
        _u = self.edtUser.GetValue()
        _p = self.edtPass.get_edit_text()
        _c = pyGestorModel.proxies.DB_Procedures.sproc_autenticalogin({'user': _u, 'pass': _p})
        if _c:
            self._widgetsession._login(_u)
            self._widgetsession.UnShowWidget()
        else:
            self._widgetprocessa(conf.cmds.dlg_statusbar_change,
                                 "Usuário ou Senha Incorretos")
            self.act_Clear()

    def act_Clear(self):
        self.edtPass.set_edit_text('')
        self.edtUser.setValue(None, force=True)
        self._lw.set_focus(0)

    def callbacks(self, backref):
        if backref == 'enter':
            self.act_CheckLogin()
            return True
        if backref == 'esc':
            self.act_Clear()
            return True

    def keyHandler(self, input):
        return self.callbacks(input)

    def show(self):
        # lck = threading.Lock()

        self._widgetsession.ShowDialogWidget(self.widget, self.keyHandler, None, self,isDialog=False)

        # nisk.util.espera(lck)
