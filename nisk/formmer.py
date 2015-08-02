#!/usr/bin/python
# -*- coding: utf-8 -*-


import urwid
import nisk.TUI
import widgets, util, nsatw

import os, logging, datetime
import conf, threading


class tfld:
    textbox = 1
    itextbox = 2
    datepicker = 3
    fieldbox = 4
    checkfield = 5


class formmer(urwid.ListBox, nisk.TUI.nestedwidget):
    footer_text = []

    def __init__(self, campos=[('tipo', 'titulo', 'binding', {'opts': 'values'})]):
        nisk.TUI.nestedwidget.__init__(self)

        self.widgets = {}  # (titulo,binding, {opts}
        self.fields = {}  # (widget1,widget2...)
        self.lwlist = []
        self.isdirty = False
        self.divider = urwid.Divider(u' ')
        self.lwlist.append(self.divider)

        for x in campos:
            t = x[0]  # tipo
            c = x[1]  # caption
            b = x[2]  # binding
            o = x[3] if len(x) > 3 else {}  # options
            #
            if t == tfld.textbox:
                tf = widgets.wgtFieldBox(caption=c, bindf=b)

            elif t == tfld.itextbox:
                tf = widgets.wgtIntFieldBox(caption=c, bindf=b)

            elif t == tfld.fieldbox:
                tf = widgets.wgtFieldBoxDb(caption=c, bindf=b,
                                           ltabela=util.defaultv(o, 'ltab', ''),
                                           tabela=util.defaultv(o, 'tab', ''))
            elif t == tfld.datepicker:
                tf = widgets.wgtDateFieldBox(caption=c, bindf=b)
            else:
                continue
                #
            self.widgets[tf] = (c, b, o)
            self.lwlist.append(tf)
            self.lwlist.append(self.divider)
            #
            if self.fields.has_key(b):
                self.fields[b][0].append(tf)
            else:
                self.fields[b] = [[tf]]
                #
        # self.binder = binder(self.widgets,self.fields)
        #
        self._widgetregistrafilhos(self.lwlist)
        self.lw = urwid.SimpleListWalker(self.lwlist)
        urwid.ListBox.__init__(self, self.lw)
        logging.debug('formmer ok')

        #


        #


class binder:
    signals = ['change', 'saved']

    def __init__(self, wids={}, fields={}):

        self._dirty = False
        self.m = 1
        self._dados = {}
        self._dados_orig = {}
        self.wids = wids
        self.fields = fields
        for x in wids.keys():
            if isinstance(x, widgets.bindablefield):
                x.setOnChange(self.fieldchange_handler)
                # util.dump(x)
                x.set_bindf(wids[x][1])
            else:
                logging.debug('binder wid error1')
                #

    def load(self, dados, isreload=False):
        self._dados = dados
        if not isreload:
            self._dados_orig = dados.copy() if isinstance(dados, dict) else util.row2dict(dados)

        self.m = 1 if isinstance(dados, dict) else 0

        for x in self.wids.keys():
            try:

                if isinstance(x, widgets.bindablefield):
                    b = x.get_bindf()

                    v = dados[b] if self.m else getattr(dados, b)

                    x.setValue(v)
                else:
                    logging.debug('binder wid error2')
            except Exception, e:
                logging.exception(e)

    def update(self):
        self.m = 1 if isinstance(self._dados, dict) else 0

        for x in self.wids.keys():
            try:
                if isinstance(x, widgets.bindablefield):
                    b = x.get_bindf()
                    v = x.GetValue()

                    if self.m:
                        self._dados[b] = v
                    else:
                        # util.dump(self._dados)
                        # util.dump(b)
                        # util.dump(v)
                        # util.dump(getattr(self._dados, b))
                        setattr(self._dados, b, v)
            except Exception, e:
                logging.exception(e)
                # b = x.get_bindf()
                # v = x.GetValue()
                # util.dump(self._dados)
                # util.dump(b)
                # util.dump(v)
                # util.dump(getattr(self._dados, b))

    def abort(self):
        self.consultor.revertItem()
        self.clearForm()
        self.set_isdirty(False)

    def clearForm(self):
        self.load(self._dados_orig, isreload=1)

    def get_isdirty(self):
        return self._dirty

    def set_isdirty(self, isdirty):
        x = 1 if self._dirty != isdirty else 0
        self._dirty = isdirty
        if x:
            urwid.emit_signal(self, 'change', self)

    def valida(self):
        pass

    def fieldchange_handler(self, x, d, *arg):
        try:
            if isinstance(x, widgets.bindablefield):
                v = x.GetValue()
                b = x.get_bindf()
                if self.m:
                    self._dados[b] = v
                else:
                    setattr(self._dados, b, v)
            else:
                logging.debug('binder wid error3')
        except Exception, e:
            logging.exception(e)

        self.set_isdirty(True)
        logging.debug('dirty setado')
        # util.dump((x,d,x.get_bindf()),'cod setado')

    def onAdd(self, evt):
        pass

    def onUpdate(self, evt):
        pass

    def onCancel(self, evt):
        pass
