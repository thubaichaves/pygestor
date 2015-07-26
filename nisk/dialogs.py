#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import thread
import logging
import conf
import nisk
import time, datetime
import nisk.util
import nisk.TUI
from nsatw import *
from urwid import *
import math
import urwid


######################################################################
class StatusBar(urwid.AttrMap):
    lblRelogio = None
    lblInfo = None

    def __init__(self, parent):
        self.lblInfo = urwid.Text('', align='center')
        self.info = None
        self.statusbar = urwid.Pile([('pack', self.lblInfo)])
        # self.statusbar = urwid.Text('xxxx', align='center')
        self.lblRelogio = urwid.Text(time.strftime('%H:%M:%S'), align='center')
        self.lblRelogio_w = urwid.AttrWrap(self.lblRelogio, 'Relogio')
        self._pilhaInfo = nisk.util.pilha()
        self.col = urwid.Columns([self.statusbar, ('fixed', 10, self.lblRelogio_w)])

        super(StatusBar, self).__init__(self.col, 'InfoFooter')

    def popInfo(self):
        self.info = None if self._pilhaInfo.vazia() else  self._pilhaInfo.desempilha()
        self.info = '' if self.info == None else self.info

        self.lblInfo.set_text(self.info)

    def putInfo(self, info):
        self._pilhaInfo.empilha(self.info)
        self.info = info
        self.info = '' if self.info == None else self.info

        self.lblInfo.set_text(self.info)

    def changeInfo(self, info):
        self.info = info
        self.info = '' if self.info == None else self.info

        self.lblInfo.set_text(self.info)

    def alarmou(self, xxx=None, yyy=None):
        self.lblRelogio.set_text(time.strftime('%d/%m/%y\n%H:%M:%S'))
        # tui.mdi.loop.set_alarm_in(1, self.alarmou, None)


######################################################################
class widgetBase(urwid.Frame, nisk.TUI.nestedwidget):
    def __init__(self):
        self.statusBar = StatusBar(self)
        self.txt = urwid.Text('')
        cbox = urwid.Columns([('weight', 1, self.txt)], dividechars=3)
        super(widgetBase, self).__init__(urwid.Filler(cbox), footer=self.statusBar, focus_part='body')

    def keyHandler(self, input):
        pass

    def _widgetonshow(self):
        nisk.TUI.nestedwidget._widgetonshow(self)

    def _widgetonunshow(self):
        nisk.TUI.nestedwidget._widgetonunshow(self)

    @staticmethod
    def newSession():
        x = nisk.dialogs.widgetBase()
        y = nisk.tui.mdi.session_new(x, x.keyHandler)
        nisk.tui.mdi.session_restore(y)
        x._widgetonshow()
        # raise 'todo'


######################################################################
class GenericDialogx(WidgetWrap, nisk.TUI.nestedwidget):
    # LineBox):
    def __init__(self, widgets_lst, title, _widgetpai, style=None, **kwargs):

        self._widgetregistrapai(_widgetpai)
        self.result = dlger.void

        if style is None:
            style = []
        # frame_header = urwid.AttrMap(urwid.Text(title, 'center'), 'title')

        buttons = None

        ok_cb = kwargs['ok_cb'] if kwargs.has_key('ok_cb') else self.cb_ok
        cancel_cb = kwargs['cancel_cb'] if kwargs.has_key('cancel_cb') else self.cb_cancel

        if "OK/CANCEL" in style:
            cancel_arg = [kwargs['cancel_value']] if kwargs.has_key('cancel_value') else []
            ok_arg = [kwargs['ok_value']] if kwargs.has_key('ok_value') else []
            buttons = [
                urwid.Button(("Ok"), ok_cb, *ok_arg),
                urwid.Button(("Cancelar"), cancel_cb, *cancel_arg), ]

        elif "YES/NO" in style:
            yes_arg = [kwargs['yes_value']] if kwargs.has_key('yes_value') else []
            no_arg = [kwargs['no_value']] if kwargs.has_key('no_value') else []
            buttons = [urwid.Button(("Yes"), kwargs['yes_cb'], *yes_arg),
                       urwid.Button(("No"), kwargs['no_cb'], *no_arg)]
        if "OK" in style:
            ok_arg = [kwargs['ok_value']] if kwargs.has_key('ok_value') else []
            buttons = [urwid.Button(("Ok"), ok_cb, *ok_arg)]
        if buttons:
            buttons_flow = urwid.GridFlow(buttons, max([len(button.get_label()) for button in buttons]) + 4, 1, 1,
                                          'center')
        body_content = urwid.SimpleListWalker(widgets_lst)
        self.frame_body = UnselectableListBox(body_content)
        self.frame = FocusFrame(self.frame_body, None, buttons_flow if buttons else None,
                                'footer' if buttons else 'body')
        decorated_frame = nisk.widgets.LineBox(self.frame, title=title)
        urwid.WidgetWrap.__init__(self, decorated_frame)
        # super(GenericDialogx, self).__init__(frame)

    def cb_ok(self, xx=None, yy=None):
        self.result = dlger.ok
        self._widgetsession.UnShowWidget()

    def cb_cancel(self, xx=None, yy=None):
        self.result = dlger.cancel
        self._widgetsession.UnShowWidget()

    def khdl(self, input):
        if input in ('esc', 'Esc'):
            self.cancel_cb(None)

        if input in ('Enter', 'enter'):
            self.ok_cb(None)

        return True

    def showwidget(self, lck):
        overvars = urwid.Overlay(urwid.AttrWrap(self, 'PopupMessageBg')
                                 , self._widgetgetsession().mainframe.body, 'center', 40, 'middle', 20)
        self._widgetgetsession().ShowDialogWidget(overvars, self.khdl, lck, _nestedwidget=self._widgetpai)

    @staticmethod
    def dialog_ShowText(texto, _widgetpai, title='Alerta'):
        dlgInput.show(texto, _widgetpai, isdialog=False)


######################################################################
class InputDialogx(GenericDialogx):
    """Dialog with an edit box"""

    def __init__(self, title, instrucions, _widgetpai, style=None, default_txt='', **kwargs):
        if style is None:
            style = ['OK/CANCEL']
        instr_wid = urwid.Text(instrucions + ':')
        self.edit_box = AdvancedEdit(edit_text=default_txt)
        self.edit_box.set_edit_text(default_txt)
        GenericDialogx.__init__(self, [instr_wid, self.edit_box], title, _widgetpai, style=style,
                                ok_value=self.edit_box, **kwargs)
        self.frame.focus_position = 'body'


######################################################################
class dlgInput(nisk.TUI.nestedwidget):
    def __init__(self, title, instrucions, _widgetpai, default_txt='', tocall=None,params=None):
        # self.lck = threading.Lock()
        self.result = None
        self.params = params
        self.tocall = tocall
        self.rdata =None
        self._widgetregistrapai(_widgetpai)
        self.d = InputDialogx(title, instrucions, self,
                              default_txt=default_txt, ok_cb=self.ok_cb, cancel_cb=self.cancel_cb)

    def khdl(self, input):
        if input in ('esc', 'Esc'):
            self.cancel_cb(None)

        if input in ('Enter', 'enter'):
            self.ok_cb(None)

        return True

    def ok_cb(self, xx=None, yy=None):
        self.result = dlger.ok
        self.rdata = self.d.edit_box.get_edit_text()
        self._widgetsession.UnShowWidget()

    def cancel_cb(self, xx=None, yy=None):
        self.result = dlger.cancel
        self._widgetsession.UnShowWidget()

    def gett(self):
        r = not self.lck.acquire(False)
        # log logging.debug('gett - %s' % str(r))
        return r

    def _widgetonshow(self):
        nisk.TUI.nestedwidget._widgetonshow(self)

    def _widgetonunshow(self):
        nisk.TUI.nestedwidget._widgetonunshow(self)
        if self.tocall:
            self.tocall((self.result, self.rdata,self.params))

    def showwidget(self, lck, _widgetpai, isdialog=True):
        overvars = urwid.Overlay(urwid.AttrWrap(self.d, 'PopupMessageBg')
                                 , self._widgetgetsession().mainframe.body, 'center', 40, 'middle', 20)

        self._widgetgetsession().ShowDialogWidget(overvars, self.khdl, lck, _nestedwidget=self, isDialog=isdialog)

    @staticmethod
    def show(instrucions, _widgetpai, title='Neon Gestor', default_txt='', tocall=None, isdialog=True):
        if isdialog:
            # log logging.debug('1 - %s' % util.timestampf())
            d = dlgInput(title, instrucions, _widgetpai=_widgetpai, default_txt=default_txt)

            # logging.debug('2 - %s' % nisk.util.timestampf())
            lck = threading.Lock()

            # logging.debug('3 - %s' % nisk.util.timestampf())
            d.showwidget(lck, _widgetpai)

            # logging.debug('4 - %s' % util.timestampf())
            nisk.util.espera(lck)

            # logging.debug('5 - %s' % nisk.util.timestampf())
            r = d.d.edit_box.get_edit_text()

            # log logging.debug('6 - %s' % util.timestampf())
            return r, d.result

        else:
            d = dlgInput(title, instrucions, _widgetpai=_widgetpai, default_txt=default_txt, tocall=tocall)
            lck = None
            d.showwidget(lck, _widgetpai, isdialog=isdialog)
            # r = d.d.edit_box.get_edit_text()


######################################################################
class dlger(nisk.TUI.nestedwidget):
    # resultados:
    void = i = 0
    ok = i = i + 1
    cancel = i = i + 1
    yes = i = i + 1
    no = i = i + 1
    back = i = i + 1
    custom = i = i + 1

    def __init__(self):
        self.r = dlger.void
        self.rdata = {}

    def unhandled_input(self, k):
        if (k == 'esc'):
            self.r = dlger.cancel
            self._widgetsession.UnShowWidget()
            return
