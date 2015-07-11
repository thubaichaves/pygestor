#!/usr/bin/python
# -- coding: utf-8 --

import logging
import urwid
import nisk
import conf
import nisk.util
import nisk.TUI
import controller
import pyGestorForms.frmMain


class app:
    sessions = []

    @staticmethod
    def Inicia():
        mainform = pyGestorForms.frmMain.WxApp()
        nisk.TUI.tui._getInstance(mainframe=mainform, unhandled_input=mainform.keyHandler, khdl_app=app.keyHandler)

        app_ = controller.pyGestorFacade.getInstance()
        app_._widgetregistrapai(mainform)
        mainform._widgetfacade = app_
        app_.sendNotification(conf.cmds.STARTUP, nisk.tui.mdi)

        nisk.tui.mdi.run()

    @staticmethod
    def send(name, body=None, ses=None):
        raise 'facade não iniciado'
        if controller.pyGestorFacade.fac:
            controller.pyGestorFacade.fac.sendNotification(name, body)
        else:
            raise 'facade não iniciado'


    @staticmethod
    def keyHandler(input):
        if input in ('f12', 'F12'):
            nisk.tui.mdi.session_next()
            # logging.debug('nisk.tui.mdi.nextSession()')
            return True
        #
        if input in ('ctrl f12', 'ctrl F12'):
            nisk.util.abreGestor()
            return True
        #
        if input in ('f11', 'F11'):
            x = pyGestorForms.frmMain.WxApp()
            y = nisk.tui.mdi.session_new(x, app.keyHandler)
            nisk.tui.mdi.session_restore(y)
            return True
        #
        return False

