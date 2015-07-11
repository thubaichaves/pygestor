#!/usr/bin/python
# -*- coding: utf-8 -*-

from nisk import *
from nisk.nsatw import *
from nisk.formmer import tfld
import nisk.dialogs

import imprimir
import urwid
import pyGestorModel
import conf
import app


class crtl_contatos:
    @staticmethod
    def actAdd(_widgetpai, params):
        util.TerminalLogger.setup()

        txt = util.defaultv(params, 'nome', '').title()

        nome, rr = nisk.dialogs.dlgInput.show('Qual o Nome Completo do novo Contato?', _widgetpai=_widgetpai,
                                              default_txt=txt)

        if nome and rr == dlger.ok:
            nome = nome.title()

            telefones = []
            telefone = True
            while rr != dlger.cancel and telefone:
                telefone, rr = nisk.dialogs.dlgInput.show(
                    "Informe um telefone ou email para '%s'\n\r(%i adicionados)" % (nome, len(telefones)),
                    _widgetpai=_widgetpai)
                if telefone and rr == dlger.ok:
                    telefones.append(telefone)

            x = pyGestorModel.contatos_Proxy()
            y = x.getNovo(params={},dados={'nome': nome, 'telefones': telefones})

        cb = util.defaultv(params, 'callback', None)
        if cb:
            cb({'act': 'add', 'nome': nome})

    @staticmethod
    def actOpen(_widgetpai, params):
        util.TerminalLogger.setup()

        osn = nisk.util.defaultv(params, 'id', None)

        if not osn:
            osn, rr = nisk.dialogs.dlgInput.show('Abrir Contato por Código', _widgetpai)

        w = formmer_contatos_edit(params={'id': util.asInt(osn)})
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

    def show(self):
        x = self.binder.consulta(self.params)
        if x:
            self._widgetsession.ShowDialogWidgetOverlay(self.get_frame(), v_hdlr=self.unhandled_input,
                                                        _nestedwidget=self)
        else:
            self._widgetprocessa(conf.cmds.dlg_statusbar_put, (('error'), 'Não foi possível abrir essa OS'))
            # nisk.dialogs.dlgInput.show(conf.textos['crtl_os.erro_abriros'],self._widgetpai)
            nisk.dialogs.dlgInput.show(conf.textos['crtl_os.erro_abriros'], self._widgetpai)
            self._widgetprocessa(conf.cmds.dlg_statusbar_pop)


class mediator_contatos(pyGestorModel.mediator_base):
    def __init__(self, f):
        super(mediator_contatos, self).__init__(f, pyGestorModel.contatos_Proxy(), 'mediator_contatos')
