# encoding: utf-8

"""
Example application for integrating serving a Urwid application remotely.

Run this application with::

    twistd -ny example.tac

Then in another terminal run::

    ssh -p 6022 user@localhost

(The password is 'pw' without the quotes.)

Note: To use this in real life, you must use some real checker.
"""

from twisted.cred.checkers import InMemoryUsernamePasswordDatabaseDontUse,AllowAnonymousAccess

from txurwid import UrwidMind, UrwidUi, create_application,TwistedScreen,TwistedSharedEventLoop
import logging
import urwid
import nisk
import app
import conf
import nisk.util
import nisk.TUI
import controller
import pyGestorForms.frmMain

class HelloUi(UrwidUi):

    def __init__(self, urwid_mind):
        self.mind = urwid_mind
        self.toplevel = self.create_urwid_toplevel()
        self.palette = self.create_urwid_palette()
        self.screen = TwistedScreen(self.mind.terminalProtocol)
        self.loop = self.create_urwid_mainloop()

    def create_urwid_palette(self):
        return conf.const_PALETTE

    def unhandled_input(self,key):
                k = self.mind.unhandled_key(key)
                if k:
                    k = self.toplevel.keyHandler(k)
                return

    def create_urwid_mainloop(self):
        t =nisk.TUI.tui(
            mainframe=self.toplevel,screen=self.screen, unhandled_input=self.unhandled_input, khdl_app=app.keyHandler,
            colors= self.palette,eventloop=TwistedSharedEventLoop()
        )

        # if nisk.TUI.tui.mdi is None:
        nisk.TUI.tui.mdi = t

        app_ = controller.pyGestorFacade.getInstance()
        app_._widgetregistrapai(self.toplevel)
        self.toplevel._widgetfacade = app_
        app_.sendNotification(conf.cmds.STARTUP, nisk.tui.mdi)

        loop = t.loop
        self.screen.loop = loop
        # loop.run()
        nisk.tui.mdi.run()
        return loop

    def create_urwid_toplevel(self):
        mainform = pyGestorForms.frmMain.WxApp()
        return mainform


class HelloMind(UrwidMind):
    ui_factory = HelloUi
    cred_checkers = [InMemoryUsernamePasswordDatabaseDontUse(user='pw'),AllowAnonymousAccess()]
    # cred_checkers = [AllowAnonymousAccess()]


application = create_application('TXUrwid Demo', HelloMind, 6022)

# vim: ft=python

