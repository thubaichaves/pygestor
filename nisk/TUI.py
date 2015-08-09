#!/usr/bin/python
# -*- coding: utf-8 -*-


import logging
import time
import threading
import sys

import urwid
import util
import conf


######################################################################
class tui:
    mdi = None
    signal_handled = None

    def __init__(self, mainframe=None, screen=None, unhandled_input=None, khdl_app=None, colors=conf.const_PALETTE, eventloop=None):

        self._setupSIGINTprocess()

        self.mainframe = mainframe
        self.inputhadler = unhandled_input

        self.running = False
        self.seslocker = threading.Lock()

        if not screen:
            import urwid.curses_display
            screen = urwid.curses_display.Screen()
            # screen = urwid.raw_display.Screen()
            # screen.set_terminal_properties(256)

        import urwid
        self.loop = urwid.MainLoop(mainframe, colors, screen=screen, unhandled_input=self._khdl,
                                   pop_ups=True, input_filter=self._inputfilter,event_loop=eventloop)

        self.loop.set_alarm_in(0.1, self._sndloop, None)

        self.khdl_app = khdl_app

        self.sessions = {}
        self.lastsession = 0
        self.sesspos = 0
        self.session_restore(self.session_new(mainframe, unhandled_input))
        self.mainframe._widgetsession = self.currentsession

    def session_restore(self, sessionN):
        self.seslocker.acquire(False)
        self.currentsession = self.sessions[sessionN]  # session(1, 1, 1, 1)  #
        self.session = self.currentsession.sessionid
        self.inputhadler = self.currentsession.inputhadler
        self.loop.widget = self.currentsession.mainframe

        self.sesspos = self.sessions.keys().index(self.session)

        try:
            self.seslocker.release()
        except:
            pass

    def session_next(self):
        self.sesspos = self.sesspos + 1 if self.sesspos + 1 < len(self.sessions) else 0
        self.session_restore(self.sessions.keys()[self.sesspos])

    def session_new(self, mainform, hdlr):
        self.lastsession = self.lastsession + 1
        self.sessions[self.lastsession] = session(self.lastsession, mainform, hdlr, loop=self.loop)
        return self.lastsession

    def run(self):
        if not self.running:
            self.running = True
            self.currentsession.mainframe._widgetonshow()
            self.loop.run()

    def stop(self):
        # os.close(self.Pipe)
        # self.loop.stop()
        raise urwid.ExitMainLoop()
        sys.exit(0)

    def khdl(self, input):
        if input in ('esc', 'ESC', 'enter'):
            # logging.debug('esc unshow')
            self.currentsession.UnShowWidget()
            return True
        return False

    def _khdl(self, input):
        r = self.currentsession._khdl(input)
        if r:
            return r

        if self.khdl_app:
            r = self.khdl_app(input)
            if r:
                return r
        return self.khdl(input)

    def _inputfilter(self, input, args):
        self.currentsession._inputfilter(input, args)
        try:
            pass
        except:
            logging.debug('_inputfilter')

        return input

    def _sndloop(self, xxx, yyy):
        if self.seslocker.acquire(False):
            self.seslocker.release()
            self.currentsession._processa_topwidget()
        else:
            logging.debug('?')

        self.loop.set_alarm_in(0.1, self._sndloop, None)

    @staticmethod
    def _getInstance(mainframe=None, unhandled_input=None, khdl_app=None):
        t = tui(mainframe=mainframe, unhandled_input=unhandled_input, khdl_app=khdl_app)

        if tui.mdi is None:
            tui.mdi = t
        return t

    ### Processa CRTL-C
    @staticmethod
    def _setupSIGINTprocess():
        def signal_handler(signal, frame):
            raise urwid.ExitMainLoop()
            sys.exit(0)
            pass

        def signal_handler2(signal, frame):
            return False

        if tui.signal_handled is None:
            #todo
            # signal.signal(signal.SIGINT, signal_handler)
            # signal.signal(signal.SIGTSTP, signal_handler2)
            tui.signal_handled = 1


######################################################################
class session:
    def __init__(self, sessionid, mainframe, inputhadler, widget=None, params=None, loop=None):
        self.sessionid = sessionid
        self.PilhaWidget = util.pilha()
        self.PilhaDialogs = util.pilha()
        self.locker = None
        self._seslocker = threading.Lock()
        self.inputhadler = inputhadler
        self.widget = widget
        self.mainframe = mainframe
        self.params = params
        self.nestedwidget = mainframe
        self._logout_time = 30
        self._loop = loop

    def _widget_show(self, v_wgt, v_hdlr, vlocker=None, _nestedwidget=None):
        if not v_wgt is None:
            self.PilhaWidget.empilha((self.mainframe.body, self.inputhadler, self.locker, self.nestedwidget))

            self.mainframe.body = v_wgt
            self.inputhadler = v_hdlr
            self.locker = vlocker
            self.nestedwidget = _nestedwidget

            if isinstance(self.nestedwidget, nestedwidget):
                self.nestedwidget._widgetonshow()
            return
        logging.debug('ShowWidget bad - %s' % v_wgt.__class__.__name__)

    def _processa_topwidget(self):
        if len(self.PilhaDialogs.dados) > 0:
            v_wgt, v_hdlr, locker, _nestedwidget = self.PilhaDialogs.desempilha()
            self._widget_show(v_wgt, v_hdlr, vlocker=locker, _nestedwidget=_nestedwidget)

    def _khdl(self, input):
        r = None
        if not self.inputhadler is None:
            # logging.debug('key 1:'+input)
            r = self.inputhadler(input)
            if r:
                return r
        for x in self.PilhaWidget.dados:
            # logging.debug('key 2:'+input)
            if not x is None:
                r = x[1](input)
                if r:
                    return r

    def _logout(self, p=None, q=None):
        self._logout_time = self._logout_time - 10
        if self._logout_time < 1:
            if isinstance(self.nestedwidget, nestedwidget):
                self.nestedwidget._widgetprocessa(conf.cmds.cmd_checkLogin)
            #util.dump([self._logout_time, self._usr, 'loged out'])
        else:
            self._loop.set_alarm_at(time.time() + 10, self._logout)
        #util.dump([self._logout_time, self._usr, 'logout'])

    def _login(self, usr):
        self._usr = usr
        self._logout_time = 30
        #util.dump([self._logout_time, self._usr, 'login'])
        self._logout()

    def _inputfilter(self, input, args):
        if input==['ctrl c']:            
            #raise 'ctrl c'
            raise urwid.ExitMainLoop()
            sys.exit(0)
        if input:
            self._logout_time = 30
        return input

    def ShowDialogWidget(self, v_wgt, v_hdlr, vlocker, _nestedwidget, isDialog=True):
        if isDialog:
            self.PilhaDialogs.empilha((v_wgt, v_hdlr, vlocker, _nestedwidget))
        else:
            self._widget_show( v_wgt, v_hdlr, vlocker, _nestedwidget)

    def ShowDialogWidgetOverlay(self, v_wgt, v_hdlr, _nestedwidget, isdialog=True):
        bkg = v_wgt  # urwid.AttrWrap(w, 'PopupMessageBg')

        if v_hdlr is None:
            v_hdlr = self._khdl

        sx = conf.sizes['ListBrowser1']

        x = len(self.PilhaDialogs.dados)

        over = urwid.Overlay(bkg, self.mainframe.body, ('fixed left', 8 + x), sx[1], sx[2], sx[3])

        lck = threading.Lock()
        self.ShowDialogWidget(over, v_hdlr, lck, _nestedwidget, isDialog= isdialog)
        if isdialog:
            util.espera(lck)
        #

    def UnShowWidget(self):
        if not self.PilhaWidget.vazia():
            if not self.locker is None:
                if not self.locker.acquire(False):
                    self.locker.release()

            tocall = self.nestedwidget

            old = self.PilhaWidget.desempilha()
            self.mainframe.body = old[0]
            self.inputhadler = old[1]
            self.locker = old[2]
            self.nestedwidget = old[3]

            if isinstance(tocall, nestedwidget):
                tocall._widgetonunshow()


######################################################################
class nestedwidget:
    _widgetpai = None
    _widgetfacade = None
    _widgetfilhos = []
    _widgetsession = None

    def __init__(self, pai=None, filhos=[]):
        self._widgetpai = pai
        self._widgetgetsession()
        self._widgetregistrafilhos(filhos)

    def _widgetprocessa(self, mensagem, dados=None, origem=None):
        if not origem:
            origem = self

        if self._widgetfacade:
            return self._widgetfacade._widgetprocessa(mensagem, dados, origem)
        elif self._widgetpai:
            return self._widgetpai._widgetprocessa(mensagem, dados, origem)
        raise '_widgetprocessa'

    def _widgetinformafilhos(self, mensagem, dados=None, origem=None):
        for x in filhos:
            try:
                x._widgetinformafilhos(mensagem, dados, origem)
            except:
                pass

    # def _widgetfacade(self):
    #     if _widgetfacade:
    #         return _w
    #     if self._widgetpai is None:
    #         return None
    #     return self._widgetpai._widgetfacade()

    def _widgetregistrafilhos(self, filhos):
        for x in filhos:
            try:
                x._widgetregistrapai(self)
                if not x in self._widgetfilhos:
                    self._widgetfilhos.append(x)
            except:
                pass

    def _widgetregistrapai(self, pai):
        self._widgetpai = pai
        self._widgetgetsession()

    def _widgetonshow(self):
        pass

    def _widgetonunshow(self):
        pass

    def _widgetshowfilhos(self):
        for x in filhos:
            try:
                x._widgetonshow()
            except:
                pass

    def _widgetunshowfilhos(self):
        for x in filhos:
            try:
                x._widgetonunshow()
            except:
                pass

    def _widgetgetsession(self):
        if not self._widgetsession and self._widgetpai:
            self._widgetsession = self._widgetpai._widgetgetsession()

        return self._widgetsession
