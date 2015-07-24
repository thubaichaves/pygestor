#!/usr/bin/python
# -*- coding: utf-8 -*-

import urwid

from nisk import *
from nisk.nsatw import *
from nisk.formmer import tfld
import nisk.dialogs
import pyGestorModel
import conf
from nisk.TUI import nestedwidget


class contatos_new(nestedwidget):
    def __init__(self, _widgetpai, params):
        contatos_new.scancela = step = 0
        #
        contatos_new.sstart = step = step + 1
        contatos_new.snome = step = step + 1
        contatos_new.stelefone = step = step + 1
        contatos_new.sedita = step = step + 1
        #
        contatos_new.sfim = step = step + 1
        #
        self.step = contatos_new.sstart
        self.r, self.s = None, None

        self.telefone = True
        self.dados = {
            "telefones": []
        }

        nestedwidget.__init__(self, _widgetpai)

        self.params = params
        self._p_cb = util.defaultv(params, 'callback', None)
        self._p_txt = util.defaultv(params, 'nome', '').title()

    def callback(self, data=None):
        self.r=None

        if self.step == contatos_new.snome:
            (self.r, self.dados['nome'],z) = data

        elif self.step == contatos_new.stelefone:
            (xr, telefone,z) = data
            if telefone and xr == dlger.ok:
                self.dados['telefones'].append(telefone)
            else:
                self.step = self.step + 1
            #
        elif self.step == contatos_new.sedita:
            (self.r, self.dados['nome'],z) = data
            #


        if self.r == dlger.ok:
            self.step = self.step + 1
        elif self.r == dlger.back:
            self.step -= 1
        elif self.r == dlger.cancel:
            self.step = contatos_new.scancela
            #
        x = 1
        while x:
            x = self.step_x(self.step)

    def step_x(self, step, data=None):
        if step == contatos_new.sstart:
            self.step = contatos_new.snome
            return 1
            #
        elif step == contatos_new.snome:
            nisk.dialogs.dlgInput.show('Qual o Nome Completo do novo Registro?', _widgetpai=self._widgetpai,
                                       default_txt=self._p_txt, isdialog=False, tocall=self.callback)
            return
            #
        elif step == contatos_new.stelefone:
            nisk.dialogs.dlgInput.show(
                "Informe um telefone ou email para '%s'\n\r(%i adicionados)" % (
                self.dados['nome'], len(self.dados['telefones'])),
                _widgetpai=self._widgetpai, isdialog=False, tocall=self.callback)
            return
            #
        elif step == contatos_new.sedita:

            x = pyGestorModel.contatos_Proxy()
            y = x.getNovo(params={}, dados=self.dados)

            w = formmer_contatos_edit(
                params={'new': True, 'dados': self.dados},
                dados=self.dados)
            w._widgetregistrapai(self._widgetpai)
            w.show(isdialog=False)
            return
            #
        elif step == contatos_new.sfim:
            if self._p_cb:
                self._p_cb({'act': 'add', 'nome': self._p_nome})
            self.step = None
            return
            #
        elif step == contatos_new.scancela:
            self._widgetsession.UnShowWidget()
            self.step = None
        return 0

    def act_start(self):
        x = 1
        while x:
            x = self.step_x(self.step)


class contatos_open(nestedwidget):
    def __init__(self, _widgetpai, params):
        contatos_open._cancela = step = 0
        contatos_open._start = step = step + 1
        contatos_open.sopen = step = step + 1
        contatos_open._fim = step = step + 1
        #
        self.step = contatos_open._start
        self.r, self.s = None, None
        self.dados = {}

        nestedwidget.__init__(self, _widgetpai)
        self.params = params
        self._p_cb = util.defaultv(params, 'callback', None)
        self._p_txt = util.defaultv(params, 'nome', '').title()

    def callback(self, data=None):

        if self.step == contatos_open._start:
            self.step = self.step + 1
        if self.step == contatos_open._start:
            (self.r, self.dados['osn'],z) = data

        if self.r == dlger.ok:
            self.step = self.step + 1
        elif self.r == dlger.back:
            self.step -= 1
        elif self.r == dlger.cancel:
            self.step = contatos_open._cancela

        x = 1
        while x:
            x = self.step_x(self.step)

    def step_x(self, step, data=None):

        if step == contatos_open._start:
            osn = nisk.util.defaultv(self.params, 'id', None)
            self.step = contatos_open.sopen
            return 1

        if step == contatos_open.sopen:
            self.w = formmer_contatos_edit(params=self.params)
            self.w._widgetregistrapai(self._widgetpai)
            self.w.show()
            return

        if step == contatos_open._fim:

            nome = None
            try:
                nome = self.w.binder._dados.nome
            except:
                pass

            cb = util.defaultv(self.params, 'callback', None)
            if cb:
                cb({'act': 'open', 'nome': nome})
            return

        if step == contatos_open._cancela:
            self._widgetsession.UnShowWidget()
            return

    def act_start(self):
        x = 1
        while x:
            x = self.step_x(self.step)


class formmer_contatos_edit(formmer.formmer, dlger):
    # text_button_list = [('key', ['M', ('title', "emu"), "F1"]), ]
    text_button_list = []

    def __init__(self, params, dados=None):
        self.params = params
        self.cc = nisk.widgets.HMenu(conf.menu_contatos_edit, None, defaultcb=self.callbacks, width=24, selfclose=True)

        formmer.formmer.__init__(self, [
            (tfld.textbox, 'Nome', 'alias'),
            (tfld.textbox, 'Nome Completo', 'nomec'),
        ])
        self.binder = mediator_contatos(self)

    def callbacks(self, backref):
        # -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
        if backref == 'saveorabort':
            self.binder.update()
            nisk.dialogs.GenericDialogx.dialog_ShowText('Salvo! ', self)
            return True
        # -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
        elif backref == 'abort':
            self.binder.abort()
            nisk.dialogs.GenericDialogx.dialog_ShowText('Desfeitas Alterações! ', self)
            return True
        # -   -   -   -   -   -   -   -   -   -   -   -   -   -   -
        elif backref == 'save':
            self.binder.update()
            nisk.dialogs.GenericDialogx.dialog_ShowText('Salvo! ', self)
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

        lb = urwid.AttrWrap(widgets.LineBox(self.cc, title='Contato'), 'windowsborder')
        return lb

    def show(self, isdialog=False):
        x = self.binder.consulta(self.params)
        if x:
            sx = conf.sizes['ListBrowser1']
            over = urwid.Overlay(self.get_frame(), self._widgetsession. mainframe.body,('fixed left', 8 ), sx[1], sx[2], sx[3])
            #over = urwid.Overlay(self.get_frame(), self._widgetsession. mainframe.body, 'center', ('relative', 75), 'middle',
            #                     ('relative', 75))
            self._widgetsession.ShowDialogWidget(over, self.unhandled_input, None,
                                                 _nestedwidget=self, isDialog=False)
        else:
            self._widgetprocessa(conf.cmds.dlg_statusbar_put, (('error'), 'Não foi possível abrir essa OS'))
            # nisk.dialogs.dlgInput.show(conf.textos['crtl_os.erro_abriros'],self._widgetpai)
            nisk.dialogs.dlgInput.show(conf.textos['crtl_os.erro_abriros'], self._widgetpai)
            self._widgetprocessa(conf.cmds.dlg_statusbar_pop)


class mediator_contatos(pyGestorModel.mediator_base):
    def __init__(self, f):
        super(mediator_contatos, self).__init__(f, pyGestorModel.contatos_Proxy(), 'mediator_contatos')
