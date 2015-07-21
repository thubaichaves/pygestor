#!/usr/bin/python
# -*- coding: utf-8 -*-

from nisk import *
from nisk.nsatw import *
from nisk.formmer import tfld
import nisk.dialogs

import imprimir
import urwid
import pyGestorModel
import pyGestorModel.orm_listas
from nisk.TUI import nestedwidget
import conf
import app


class crtl_listsA:
    @staticmethod
    def actAdd(_widgetpai, params):
        util.TerminalLogger.setup()

        txt = util.defaultv(params, 'nome', '').title()
        ltab = params['ltab']
        if not ltab:
            raise "tab não informada"

        nome, rr = nisk.dialogs.dlgInput.show('Qual o Nome Completo do novo Registro?', _widgetpai=_widgetpai,
                                              default_txt=txt)

        if nome and rr == dlger.ok:
            nome = nome.title()

            x = pyGestorModel.listas_Proxy(pyGestorModel.orm_listas.lists_a,ltab)
            y = x.getNovo({},dados={'nome': nome, 'ltab': ltab})

        cb = util.defaultv(params, 'callback', None)
        if cb:
            cb({'act': 'add', 'nome': nome})

    @staticmethod
    def actOpen(_widgetpai, params):
        util.TerminalLogger.setup()

        osn = nisk.util.defaultv(params, 'id', None)
        ltab = params['ltab']
        if not ltab:
            raise "tab não informada"

        # if not osn:
        #     osn, rr = nisk.dialogs.dlgInput.show('Abrir Registro por Código', _widgetpai)

        w = formmer_listsA_edit(params=params)
        w._widgetregistrapai(_widgetpai)
        w.show()

        nome = None
        try:
            nome = w.binder._dados.nome
        except:
            pass

        cb = util.defaultv(params, 'callback', None)
        if cb:
            cb({'act': 'open', 'nome': nome})


class listsA_new(nestedwidget):
    def __init__(self, _widgetpai,params):
        listsA_new.scancela = step = 0
        #
        listsA_new.sstart = step = step + 1
        listsA_new.snome = step = step + 1
        listsA_new.sedita = step = step + 1
        #
        listsA_new.sfim = step = step + 1
        #
        self.step = listsA_new.sstart
        self.r, self.s = None, None
        self.dados = {}

        nestedwidget.__init__(self, _widgetpai)

        self.params=params
        self._p_cb = util.defaultv(params, 'callback', None)
        self._p_txt = util.defaultv(params, 'nome', '').title()
        self._p_ltab = params['ltab']
        if not self._p_ltab:
            raise "tab não informada"


    def callback(self, data=None):

        if self.step == listsA_new.snome:
            (self.r, self.dados['nome']) = data
        if self.step == listsA_new.sedita:
            (self.r, self.dados['nome']) = data

        if self.r == dlger.ok:
            self.step = self.step + 1
        elif self.r == dlger.back:
            self.step -= 1
        elif self.r == dlger.cancel:
            self.step = listsA_new.scancela

        self.step_x(self.step)

    def step_x(self, step, data=None):
        if step == listsA_new.sstart:
            pass
            #
        elif step == listsA_new.snome:
            nisk.dialogs.dlgInput.show('Qual o Nome Completo do novo Registro?', _widgetpai=self._widgetpai,
                                              default_txt=txt, isdialog=False, tocall=self.callback)
            #
            #
        elif step == listsA_new.sedita:
            w = formmer_listsA_edit(params={'new': True, 'dados': self.dados}, dados=self.dados)
            w._widgetregistrapai(self._widgetpai)
            w.show(isdialog=False,)
            #
        elif step == listsA_new.sfim:
            if self._p_cb:
                self._p_cb({'act': 'add', 'nome': self._p_nome})

            #
        elif step == listsA_new.scancela:
            self._widgetsession.UnShowWidget()

    def act_start(self):
        self.step_x(self.step)

class os_open(nestedwidget):
    def __init__(self, _widgetpai):
        crtl_os.os_open._cancela = step = 0
        crtl_os.os_open.a_numero = step = step + 1
        crtl_os.os_open._fim = step = step + 1
        #
        self.step = crtl_os.os_open.a_numero
        self.r, self.s = None, None
        self.dados = {}

        nestedwidget.__init__(self, _widgetpai)

    def callback(self, data=None):

        if self.step == crtl_os.os_open.a_numero:
            (self.r, self.dados['osn']) = data

        if self.r == dlger.ok:
            self.step = self.step + 1
        elif self.r == dlger.back:
            self.step -= 1
        elif self.r == dlger.cancel:
            self.step = crtl_os.os_open._cancela

        self.step_x(self.step)

    def step_x(self, step, data=None):
        if step == crtl_os.os_open.a_numero:
            nisk.dialogs.dlgInput.show('Abrir OS', self._widgetpai, tocall=self.callback, isdialog=False)

        if step == crtl_os.os_open._fim:
            w = formmer_os_edit(params={'os': self.dados['osn']})
            w._widgetregistrapai(self._widgetpai)
            w.show()

        if step == crtl_os.os_open._cancela:
            self._widgetsession.UnShowWidget()

    def act_start(self):
        self.step_x(self.step)

class formmer_listsA_edit(formmer.formmer, dlger):
    # text_button_list = [('key', ['M', ('title', "emu"), "F1"]), ]
    text_button_list = []

    def __init__(self, params, dados=None):
        self.params = params
        # self.dados = dados
        self.cc = nisk.widgets.HMenu(conf.menu_listsA_edit, None, defaultcb=self.callbacks, width=24, selfclose=True)

        formmer.formmer.__init__(self, [
            (tfld.textbox, 'Nome', 'nome'),
            (tfld.textbox, 'Descrição', 'descr'),
        ])
        self.binder = mediator_listas(self)

    def callbacks(self, backref):
        # -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
        if backref == 'saveorabort':
            self.binder.update()
            nisk.dialogs.GenericDialogx.dialog_ShowText('Salvo! ', self)
            return True
        # -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
        elif backref == 'save':
            self.binder.update()
            nisk.dialogs.GenericDialogx.dialog_ShowText('Salvo! ', self)
            return True
        # -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
        elif backref == 'abort':
            self.binder.abort()
            nisk.dialogs.GenericDialogx.dialog_ShowText('Desfeitas Alterações! ', self)
            return True
        # -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
        elif backref == 'menu':
            self.cc.onmenuopen()
            return True
        # -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
        elif backref == 'sair':
            if self.binder.get_isdirty():
                nisk.dialogs.GenericDialogx.dialog_ShowText(
                    'É necessário salvar as alterações desse registro ou cancela-las!', self)
                # nisk.util.dump(self.binder._dirty, 'dirty')
                return True

            self._widgetsession.UnShowWidget()
            return True
        # -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
        elif 1:
            nisk.dialogs.GenericDialogx.dialog_ShowText('Não Identificado: \n' + str(backref), self)
            pass
        return True
        # -   -   -   -   -   -   -   -   -   -   -   -   -   -   -

    def unhandled_input(self, k):
        # nisk.util.dump(k)
        if k in ('esc',):
            return self.callbacks('sair')
        if k in ('enter',):
            return self.callbacks('')
        if k in ('f1', 'meta m'):
            return self.callbacks('menu')
        if k in ('f6',):
            return self.callbacks('save')
        return False
        # return nisk.widgets.dlger.unhandled_input(self, k)

    def button_press(self, *args):
        pass

    def get_frame(self):
        bkg = widgets.SBListBox(self, (u"\u2593", "handle"), (u"\u2592", "scrollbar_bg"))
        bkg = urwid.AttrWrap(bkg, 'body')
        fw = urwid.Frame(bkg)
        mt = TabsContainer()

        buttonbar = urwid.GridFlow([urwid.AttrWrap(
            CustomButton(txt, self.button_press, left_border=('scrollbar_bg', "|"), right_border=' '),
            'buttn', 'buttnf') for txt in self.text_button_list],
                                   conf.sizes['statusbarbuttonA'], 0, 0, 'left')

        mt.addTab('Básico [c-B]', fw)
        mt.addTab('Histórico [c-H]',
                  urwid.Filler(urwid.Text('xxx')))

        mt.addComplement(urwid.AttrWrap(buttonbar, 'foot'))
        ff = urwid.AttrWrap(mt, 'body')

        self.cc.setwid(mt)

        lb = urwid.AttrWrap(widgets.LineBox(self.cc, title='Registros'), 'windowsborder')
        return lb

    def show(self, isdialog=False):
        x = self.binder.consulta(self.params)
        if x:
            self._widgetsession.ShowDialogWidgetOverlay(self.get_frame(), v_hdlr=self.unhandled_input,
                                                        _nestedwidget=self, isdialog=False)
        else:
            self._widgetprocessa(conf.cmds.dlg_statusbar_put, (('error'), 'Não foi possível abrir essa OS'))
            # nisk.dialogs.dlgInput.show(conf.textos['crtl_os.erro_abriros'],self._widgetpai)
            nisk.dialogs.dlgInput.show(conf.textos['crtl_os.erro_abriros'], self._widgetpai)
            self._widgetprocessa(conf.cmds.dlg_statusbar_pop)


class mediator_listas(pyGestorModel.mediator_base):
    def __init__(self, f):
        super(mediator_listas, self).__init__(f,
                                              pyGestorModel.listas_Proxy(pyGestorModel.orm_listas.lists_a,
                                                                         f.params['ltab']),
                                                'mediator_listas')
