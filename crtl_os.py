#!/usr/bin/python
# -*- coding: utf-8 -*-


import puremvc.patterns.mediator

import nisk
import nisk.TUI
from nisk.ListBrowser import ListBrowserBase
import nisk.widgets
import nisk.dialogs
import nisk.TreeList
from pyGestorModel.orm_os import os_os
from pyGestorModel.orm_contatos import *
from nisk import *
from nisk.nsatw import *
from nisk.formmer import tfld
import nisk.dialogs
import imprimir
import urwid
import pyGestorModel
import conf
from nisk.TUI import nestedwidget
import pyGestorForms.frmListContatos
from pyGestorForms import frmListA
from sqlalchemy import *


class crtl_os:
    @staticmethod
    def actImprimeOS(_widgetpai, params):
        # sys.exit(0
        util.TerminalLogger.setup()
        imprimir.imprimir_OS.imprimir_OS(params)

    @staticmethod
    def actImprimeOS2(_widgetpai, params):
        # sys.exit(0
        util.TerminalLogger.setup()

        osn = nisk.util.defaultv(params, 'os', None)

        if not osn:
            osn, rr = nisk.dialogs.dlgInput.show('Imprimir Cumpom de Entrada de OS', _widgetpai)

        if util.canBeInt(osn):
            osn = int(osn)
            imprimir.Imprimir_EntradaOS(osn)
        else:
            nisk.dialogs.dlgInput.show('OS Inexistente', _widgetpai)

    class os_new(nestedwidget):
        def __init__(self, _widgetpai):
            crtl_os.os_new.scancela = step = 0
            crtl_os.os_new.scliente = step = step + 1
            crtl_os.os_new.stipo = step = step + 1
            crtl_os.os_new.smarca = step = step + 1
            crtl_os.os_new.sresp = step = step + 1
            crtl_os.os_new.sfim = step = step + 1
            crtl_os.os_new.simpr_a = step = step + 1
            crtl_os.os_new.simpr_b = step = step + 1
            crtl_os.os_new.spos = step = step + 1
            #
            self.step = crtl_os.os_new.scliente
            self.r, self.s = None, None
            self.dados = {}

            nestedwidget.__init__(self, _widgetpai)

        def callback(self, data=None):

            if self.step == crtl_os.os_new.scliente:
                (self.r, self.dados['cliente'], z) = data
            elif self.step == crtl_os.os_new.stipo:
                (self.r, self.dados['tipo'], z) = data
            elif self.step == crtl_os.os_new.smarca:
                (self.r, self.dados['marca'], z) = data
            elif self.step == crtl_os.os_new.sresp:
                (self.r, self.dados['usrresp'], z) = data
            elif self.step == crtl_os.os_new.sfim:
                (self.r, self.dados['os'], z) = data

            elif self.step == crtl_os.os_new.simpr_a:
                (r, qtd, z) = data
                self.r = dlger.ok
                if r and qtd > 0 and qtd < 10:
                    self._widgetprocessa(conf.cmds.cmd_os_impr, {'qtd': qtd, 'modelo': 'etiq', 'os': self.dados['os']})

            elif self.step == crtl_os.os_new.simpr_b:
                (r, qtd, z) = data
                self.r = dlger.ok
                if r and qtd > 0 and qtd < 10:
                    self._widgetprocessa(conf.cmds.cmd_os_impr,
                                         {'qtd': qtd, 'modelo': 'entrada', 'os': self.dados['os']})

            if self.r == dlger.ok:
                self.step = self.step + 1
            elif self.r == dlger.back:
                self.step -= 1
            elif self.r == dlger.cancel:
                self.step = crtl_os.os_new.scancela

            self.step_x(self.step)

        def step_x(self, step, data=None):
            if 0 > 1:
                pass
            elif step == crtl_os.os_new.scliente:
                frmc = pyGestorForms.frmListContatos.frmListContatos2({})
                frmc.Show(_widgetpai=self._widgetpai, isdialog=False, tocall=self.callback)
            elif step == crtl_os.os_new.stipo:
                w = frmListA.frmListAScreens2({'rtab': 'lists_a', 'ltab': 'ostip'})
                w.Show(_widgetpai=self._widgetpai, isdialog=False, tocall=self.callback)
            elif step == crtl_os.os_new.smarca:
                w = frmListA.frmListAScreens2({'rtab': 'lists_a', 'ltab': 'osfab'})
                w.Show(_widgetpai=self._widgetpai, isdialog=False, tocall=self.callback)
            elif step == crtl_os.os_new.sresp:
                w = frmListA.frmListAScreens2({'rtab': 'lists_a', 'ltab': 'sysus'})
                w.Show(_widgetpai=self._widgetpai, isdialog=False, tocall=self.callback)

            elif step == crtl_os.os_new.sfim:
                w = formmer_os_new(params={'new': True, 'dados': self.dados}, dados=self.dados)
                w._widgetregistrapai(self._widgetpai)
                w.show(isdialog=False, tocall=self.callback)

            elif step == crtl_os.os_new.simpr_a:
                nisk.dialogs.dlgInput.show('Imprimir quantas Etiquetas?', self._widgetpai, tocall=self.callback,
                                           isdialog=False)

            elif step == crtl_os.os_new.simpr_b:
                nisk.dialogs.dlgInput.show('Imprimir quantos Cupons?', self._widgetpai, tocall=self.callback,
                                           isdialog=False)

            elif step == crtl_os.os_new.spos:
                w = formmer_os_edit(params={'os': self.dados['os']})
                w._widgetregistrapai(self._widgetpai)
                w.show()

            elif step == crtl_os.os_new.scancela:
                self._widgetsession.UnShowWidget()

        def act_start(self):
            self.step_x(self.step)

    class os_list(nestedwidget):
        def __init__(self, _widgetpai, params=None):
            crtl_os.os_new.scancela = step = 0
            crtl_os.os_new.sstart = step = step + 1
            crtl_os.os_new.sedita = step = step + 1
            #
            self.step = crtl_os.os_new.sstart
            self.r, self.s = None, None
            self.dados = {}

            nestedwidget.__init__(self, _widgetpai)

        def callback(self, data=None):

            if self.step == crtl_os.os_new.sstart:
                (self.r, rdata, z) = data
                self.dados['os'] = util.defaultv(rdata, 'tid', None)

            if self.step == crtl_os.os_new.sedita:
                pass

            if self.r == dlger.ok:
                self.step = self.step + 1
            elif self.r == dlger.back:
                self.step -= 1
            elif self.r == dlger.cancel:
                self.step = crtl_os.os_new.scancela

            self.step_x(self.step)

        def step_x(self, step, data=None):
            if 0 > 1:
                pass
            elif step == crtl_os.os_new.sstart:
                frmc = frm_os_list({})
                frmc.Show(_widgetpai=self._widgetpai, isdialog=False, tocall=self.callback)

            elif step == crtl_os.os_new.sedita:
                w = formmer_os_edit(params={'os': self.dados['os']})
                w._widgetregistrapai(self._widgetpai)
                w.show()

            elif step == crtl_os.os_new.scancela:
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
                (self.r, self.dados['osn'], z) = data

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


class formmer_os_new(formmer.formmer):
    text_button_list = [
        ('key', [('title', " Menu "), " F1 "]),
        ('key', [('title', " Concluir "), " F6 "]),
        ('key', [('title', " Cancelar "), " ESC "])
    ]

    def __init__(self, params={}, dados={}):
        self.params = params
        self.dados = dados
        self.cc = nisk.widgets.HMenu(conf.menu_os_add, None, defaultcb=self.callbacks, width=24, selfclose=True)
        self.tocall = None
        self.r = dlger.void

        formmer.formmer.__init__(self, [
            (tfld.itextbox, 'OS', 'os', {'readonly': 1, 'estreito': 2}),
            (tfld.datepicker, 'Data de Entrada', 'dataent', {'readonly': 1, 'estreito': 2}),

            (tfld.fieldbox, 'Tipo de Equip.', 'tipo', {'ltab': 'ostip', 'estreito': 2}),
            (tfld.fieldbox, 'Marca', 'marca', {'ltab': 'osfab', 'estreito': 2}),

            (tfld.textbox, 'Modelo', 'modelo', {'estreito': 2}),
            (tfld.textbox, 'N° Série', 'ns', {'estreito': 2}),

            (tfld.fieldbox, 'Status', 'status', {'ltab': 'osstt', 'estreito': 2}),
            (tfld.fieldbox, 'Tarefa', 'ntarefa', {'ltab': 'osnxt', 'estreito': 2}),

            (tfld.fieldbox, 'Cliente', 'cliente', {'tab': 'contatos'}),
            (tfld.fieldbox, 'Telefones', ('oscliente', 't4a'), {'readonly': 1}),

            (tfld.textbox, 'Sintomas', 'sintoma'),
            (tfld.textbox, 'Acessórios', 'acess'),
            (tfld.textbox, 'Lembrete', 'lembrete'),
            (tfld.textbox, 'Estado de Conservação', 'conserva'),
            (tfld.textbox, 'Observações Internas', 'obsint'),
            (tfld.textbox, 'Observações Impressas', 'obsos'),
            (tfld.fieldbox, 'Técnico Resp.', 'usrresp', {'ltab': 'sysus'}),
        ])
        self.binder = mediator_os(self)

    def callbacks(self, backref):
        if backref in ('concluir', 'f6'):
            self.act_concluir()
            return True
        elif backref in ('cancelar', 'esc'):
            self.act_cancelar()
            return True
        else:
            # tui.mdi.ShowDialogText('Não Identificado: ' + str(backref))
            if isinstance(backref, str):
                logging.debug('Não Identificado: ' + str(backref))
            pass
        return False

    def act_sair(self):
        self._widgetsession.UnShowWidget()

    def act_cancelar(self):
        self.binder.handleCommand('cancelar')
        self.r = dlger.cancel
        self.act_sair()

    def act_concluir(self):
        self.binder.handleCommand('concluir')
        self.r = dlger.ok
        self.act_sair()

    def _widgetonunshow(self):
        if self.tocall:
            self.tocall((self.r, self.binder.dado_get('os'), self.params))
            # nisk.TUI.nestedwidget._widgetonunshow(self)

    def unhandled_input(self, k):
        if k in ('f1', 'meta m'):
            self.cc.onmenuopen()
            return True
        return self.callbacks(k)
        return False

    def button_press(self, *args):
        pass

    def get_frame(self):

        # bkg = widgets.SBListBox(self, (u"\u2593", "handle"), (u"\u2592", "scrollbar_bg"))
        bkg = nisk.widgets.SBListBox(self, (u"#", "handle"), (u"-", "scrollbar_bg"))
        bkg = urwid.Padding(widgets.SBListBox(self), left=1, right=1)
        bkg = urwid.AttrWrap(bkg, 'body')

        fw = urwid.Frame(bkg)

        bts = [urwid.AttrWrap(CustomButton(txt, self.button_press, left_border=("["), right_border="]"),
                              'buttn', 'buttnf') for txt in self.text_button_list]
        buttonbar = urwid.Pile([
            urwid.Divider('='),
            urwid.GridFlow(bts, conf.sizes['statusbarbuttonA'], 0, 0, 'left')
        ])

        mt = TabsContainer()
        mt.addTab('Básico', fw)
        mt.addTab('Pagamentos',
                  urwid.Filler(urwid.Text('IMPLANTAR')))
        mt.addComplement(urwid.AttrWrap(buttonbar, 'foot'))

        self.cc.setwid(mt)
        self.cc.onmenuopen()

        lb = urwid.AttrWrap(widgets.LineBox(self.cc, title='Nova OS'), 'windowsborder', 'windowsborder_of')
        return lb

    def show(self, isdialog=True, tocall=None):
        self.tocall = tocall
        x = self.binder.consulta(self.params)
        if x:
            self._widgetsession.ShowDialogWidgetOverlay(self.get_frame(), v_hdlr=self.unhandled_input,
                                                        _nestedwidget=self, isdialog=isdialog)

        else:
            self._widgetprocessa(conf.cmds.dlg_statusbar_put, conf.textos['crtl_os.erro_abriros'])
            nisk.dialogs.dlgInput.show(conf.textos['crtl_os.erro_abriros'], self._widgetpai)
            self._widgetprocessa(conf.cmds.dlg_statusbar_pop)


class formmer_os_edit(formmer.formmer, dlger):
    footer_text = [
        [('title', "OK"), ('key', "Enter")], "|",
        [('title', "Cancelar"), ('key', "ESC")],
    ]

    text_button_list = [
        ('key', ['M', ('title', "emu"), "F1"]),
        [('title', "OK"), ('key', "Enter")],
        ('key', ['C', ('title', "ancelar"), "ESC"]),
        'Salvar',
        'Cancelar', ]

    def __init__(self, params=None, dados=None):
        self.params = params
        self.dados = dados
        self.cc = nisk.widgets.HMenu(conf.menu_os_edit, None, defaultcb=self.callbacks, width=24, selfclose=True)

        formmer.formmer.__init__(self, [
            (tfld.itextbox, 'OS', 'os', {'readonly': 1, 'estreito': 2}),
            (tfld.datepicker, 'Data de Entrada', 'dataent', {'readonly': 1, 'estreito': 2}),

            (tfld.fieldbox, 'Cliente', 'cliente', {'tab': 'contatos'}),
            (tfld.textbox, 'Telefones', ('oscliente', 't4a'), {'readonly': 1}),

            (tfld.fieldbox, 'Status', 'status', {'ltab': 'osstt', 'estreito': 2}),
            (tfld.fieldbox, 'Tarefa', 'ntarefa', {'ltab': 'osnxt', 'estreito': 2}),

            (tfld.fieldbox, 'Tipo de Equip.', 'tipo', {'ltab': 'ostip', 'estreito': 2}),
            (tfld.fieldbox, 'Marca', 'marca', {'ltab': 'osfab', 'estreito': 2}),

            (tfld.textbox, 'Modelo', 'modelo', {'estreito': 2}),
            (tfld.textbox, 'N° Série', 'ns', {'estreito': 2}),

            (tfld.textbox, 'Acessórios', 'acess'),
            (tfld.textbox, 'Estado de Conservação', 'conserva'),
            (tfld.textbox, 'Solicitação', 'solicita'),
            (tfld.textbox, 'Sintomas', 'sintoma'),
            (tfld.textbox, u'Diagnóstico', 'diag'),
            (tfld.textbox, u'Orçamento', 'orc'),
            (tfld.textbox, 'Lembrete', 'lembrete'),
            (tfld.fieldbox, 'Técnico Resp.', 'usrresp', {'ltab': 'sysus'}),
            (tfld.textbox, 'Observações Impressas', 'obsos'),
            (tfld.textbox, 'Observações Internas', 'obsint'),
        ])
        self.binder = mediator_os(self)

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
        elif util.defaultv(backref, 0, '') == 'imprime':
            self.binder.update()
            x = util.defaultv(backref, 1, '')
            self._widgetprocessa(conf.cmds.cmd_os_impr, {'modelo': x, 'os': self.binder._dados.os})
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
            return False
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
        # bkg = widgets.SBListBox(self, (u"\u25bc", "handle"), (u"\u25b2", "scrollbar_bg"))
        bkg = urwid.Padding(widgets.SBListBox(self), left=1, right=1)
        bkg = urwid.AttrWrap(bkg, 'body')

        self._footertxb = urwid.Text(self.footer_text)
        self.footer = urwid.AttrWrap(self._footertxb, 'foot')

        # fw = widgets.LineBox(self, title='Nova OS')
        fw = urwid.Frame(bkg)
        fw.set_footer = self.footer

        mt = TabsContainer()
        mt.addTab('Básico', fw)
        mt.addTab('Informações',
                  urwid.Filler(urwid.Text('xxx')))

        buttonbar = urwid.GridFlow([urwid.AttrWrap(
            CustomButton(txt, self.button_press, left_border=('scrollbar_bg', "|"), right_border=' '),
            'buttn', 'buttnf') for txt in self.text_button_list],
                                   conf.sizes['statusbarbuttonA'], 0, 0, 'left')


        # self.menuBar = formmer_os_edit.MainMenux(tui.mdi.loop)
        # self.menuBar =MenuRoller( [('a',MainMenu(tui.mdi.loop)),('b',ProdutosMenu(tui.mdi.loop))])
        # mt.addHeader(   self.menuBar)
        mt.addComplement(urwid.AttrWrap(buttonbar, 'foot'))
        # mt.addFooter(urwid.AttrWrap(urwid.Text('blablabla'), 'foot'))
        ff = urwid.AttrWrap(mt, 'body')

        self.cc.setwid(mt)

        lb = urwid.AttrWrap(widgets.LineBox(self.cc, title='OS'), 'windowsborder', 'windowsborder_of')
        return lb

    def show(self, isdialog=False):
        x = self.binder.consulta(self.params)
        if x:
            # self._widgetsession.ShowDialogWidgetOverlay(self.get_frame(), v_hdlr=self.unhandled_input,
            #                                             _nestedwidget=self, isdialog=isdialog)
            # sx = conf.sizes['ListBrowser1']
            # over = urwid.Overlay(self.get_frame(), self._widgetsession. mainframe.body,('fixed left', 8 ), sx[1], sx[2], sx[3])
            # over = urwid.Overlay(self.get_frame(), self._widgetsession. mainframe.body, 'center', ('relative', 75), 'middle',
            #                     ('relative', 75))
            over = self.get_frame()
            self._widgetsession.ShowDialogWidget(over, self.unhandled_input, None,
                                                 _nestedwidget=self, isDialog=False)
        else:
            self._widgetprocessa(conf.cmds.dlg_statusbar_put, (('error'), 'Não foi possível abrir essa OS'))
            # nisk.dialogs.dlgInput.show(conf.textos['crtl_os.erro_abriros'],self._widgetpai)
            nisk.dialogs.dlgInput.show(conf.textos['crtl_os.erro_abriros'], self._widgetpai)
            self._widgetprocessa(conf.cmds.dlg_statusbar_pop)


class mediator_os(puremvc.patterns.mediator.Mediator, puremvc.interfaces.IMediator, nisk.formmer.binder):
    NAME = 'OSCreate'

    def __init__(self, f):
        super(mediator_os, self).__init__(mediator_os.NAME, viewComponent=None)
        nisk.formmer.binder.__init__(self, f.widgets, f.fields)
        #
        self.consultor = pyGestorModel.OS_Proxy()

    def listNotificationInterests(self):
        return []

    def handleNotification(self, note):
        pass

    def handleCommand(self, cmd, par=None):
        if cmd == 'concluir':
            self._dados.inte = 0
            self.update()

        if cmd == 'cancelar':
            self.abort()

            return
        if cmd == 'salvar':
            self.update()
            return

    def consulta(self, params={}):
        if params.has_key('new') and params.has_key('dados'):
            r = self.consultor.getNovo(params, params['dados'])
            if not r is None:
                self.load(r)
                return True

        else:
            r = self.consultor.getItem(params)
            if not r is None:
                self.load(r)
                return True

        return False

    def update(self):
        # logging.debug('update')
        nisk.formmer.binder.update(self)
        self.consultor.updateItem(self._dados)
        self.load(self._dados, isreload=True)
        self.set_isdirty(False)

    def onAdd(self, evt):
        # user = vo.UserVO(self.viewComponent.usernameInput.GetValue(),
        # self.viewComponent.user = user
        # self.userProxy.addItem(user)
        # self.sendNotification(main.AppFacade.USER_ADDED, user)
        # self.clearForm()
        pass

    def onUpdate(self, evt):
        # user = vo.UserVO(self.viewComponent.usernameInput.GetValue(),
        # self.viewComponent.firstInput.GetValue(),
        # self.viewComponent.user = user
        # self.userProxy.updateItem(user)
        # self.sendNotification(main.AppFacade.USER_UPDATED, user)
        # self.clearForm()
        pass

    def onCancel(self, evt):
        # self.sendNotification(main.AppFacade.CANCEL_SELECTED)
        # self.clearForm()
        pass



from functools import wraps
from time import time

def timed(f):
  @wraps(f)
  def wrapper(*args, **kwds):
    start = time()
    result = f(*args, **kwds)
    elapsed = time() - start
    print "%s took %f time to finish" % (f.__name__, elapsed)
    return result
  return wrapper

class frm_os_list(ListBrowserBase):
    # footer_text = []

    @timed
    def __init__(self, params):
        # self.footer_text = ''
        ListBrowserBase.__init__(self, params)

        self.headerlist = urwid.Pile([
            urwid.AttrWrap(self.header, 'head'),

            urwid.AttrWrap(wgtGridRow_oslist.getHeader(), 'head')
        ])
        self.rowheight = 3
        self.view.set_header(self.headerlist)

    @timed
    def FoolLoader(self, params):
        search = util.defaultv(params, 'search', '')
        quantos = util.defaultv(params, 'quantos', 50)
        s = pyGestorModel.dbsession.getsession()
        dados = []
        info = {}

        q = s.query(os_os).order_by(desc(os_os.os))

        search = util.asUnicode(search)

        q = q.filter(os_os.oscliente.has(contatos.nome.like('%' + search + '%')))

        q = q.limit(quantos)

        r = q.all()

        for a in r:
            try:
                dados.append({'tid': a.os, 'id': a.os, 'nome': a.oscliente.nome, 't4a': a.oscliente.t4a, 'orm': a})
            except Exception, e:
                nisk.util.dump(e)
        return {'dados': dados}

    @timed
    def load(self):
        self._params['search'] = self.search

        if self.listbox._size:
            self._params['quantos'] = self.listbox._size[1] / self.rowheight

        consulta = self.loader(self._params)

        del self.fn[:]
        dados = util.defaultv(consulta, 'dados', [])
        inv = 0
        for x in dados:
            cor = ('gridrow', 'gridrow_of') if inv % 2 else('gridrowb', 'gridrow_of')
            inv = inv + 1
            self.fn.append(wgtGridRow_oslist(dados=x, cor=cor).toappend())

        if len(self.fn) == 0:
            self.fn.append((urwid.Text(self.txt_noresults), None))

        self.completa(50)
        self.listbox.refresh()
        self.pgup()
        self._unsetdirty()

    def callback_acts(self, params={}):
        pass

    def _widgetonshow(self):
        ListBrowserBase._widgetonshow(self)
        self._widgetprocessa('dlg_statusbar_put', "Lista de OSs", self)

    def _widgetonunshow(self):
        ListBrowserBase._widgetonunshow(self)
        self._widgetprocessa('dlg_statusbar_pop')

    def unhandled_input(self, k):
        if k == "enter":
            x = self.getTid()
            if x:
                self.r = dlger.ok
                self._widgetsession.UnShowWidget()
                return True

        return ListBrowserBase.unhandled_input(self, k)


class wgtGridRow_oslist(nisk.ListBrowser.wgtGridRow):
    def __init__(self, dados=None, cor=None):
        self.cor = cor if cor else ('gridrow', 'gridrow_of')

        self._dados = dados
        if isinstance(self._dados, dict):
            self._dadosorm = util.defaultv(self._dados, 'orm', None)
        else:
            self._dadosorm = self._dados
        if not self._dadosorm:
            pass
            #raise 'data error'
        else:
            self._tid = self._dadosorm.os


        self._nome = ''

        self.load()

        urwid.AttrWrap.__init__(self, self._widget, cor[0],cor[1])

    def load(self):
        hasdata= 1 if self._dadosorm else 0
        if hasdata:
            p_os = util.astext( [(self._dadosorm,'os'),'  OS'],exact=6)
            p_cliente = util.astext( [(self._dadosorm,'oscliente','nome'),'[ Cliente]'],30)
            p_status = util.astext( [(self._dadosorm,'osstatus','nome'),'[ Cliente]'],15)
            p_tarefa = util.astext( [(self._dadosorm,'ostarefa','nome'),'[ Cliente]'],15)
            p_resp = util.astext( [(self._dadosorm,'osresp','nome'),'[ Cliente]'],15)
            p_tipo = util.astext( [(self._dadosorm,'ostipo','nome'),'[ Cliente]'],15)
            p_marca = util.astext( [(self._dadosorm,'osmarca','nome'),'[ Cliente]'],15)
            p_modelo =  util.astext( [(self._dadosorm,'osmodelo','nome'),'[ Cliente]'],15)
            p_ns  = util.astext( [(self._dadosorm,'ns'),'[ Cliente]'],10)
            p_dataent  =util.astext( [(self._dadosorm,'dataent'),'[ Cliente]'],10)
            p_datasai  =util.astext( [(self._dadosorm,'datasai'),'[ Cliente]'],10)
        else:            
            p_os = util.astext( ['  OS'],exact=6)
            p_cliente = util.astext( ['[ Cliente]'],30)
            p_status = util.astext( ['[ Situação ]'],15)
            p_tarefa = util.astext( ['[ Tarefa ]'],15)
            p_resp = util.astext( ['[ Responsável]'],15)
            p_tipo = util.astext( ['[ Tipo ]'],15)
            p_marca = util.astext( ['[ Marca ]'],15)
            p_modelo =  util.astext( ['[ Modelo]'],15)
            p_ns  = util.astext( ['[ Serial ]'],10)
            p_dataent  =util.astext( ['[ Entrada ]'],10)
            p_datasai  =util.astext( ['[ Saída ]'],10)

        self.f_os = nisk.ListBrowser.FocusableText(p_os, self.cor)
        self.f_cliente = urwid.Text(p_cliente)
        self.f_status = urwid.Text(p_status)
        self.f_tarefa = urwid.Text(p_tarefa)
        self.f_resp = urwid.Text(p_resp)
        self.f_tipo = urwid.Text(p_tipo)
        self.f_marca = urwid.Text(p_marca)
        self.f_modelo =  urwid.Text(p_modelo)
        self.f_ns  = urwid.Text(p_ns)
        self.f_dataent  = urwid.Text(p_dataent)
        self.f_datasai  = urwid.Text(p_datasai)

        self._widget = urwid.Pile([
            urwid.Columns([
                (1,urwid.Text('[')),(6,self.f_os),(2,urwid.Text('] ')),
                #
                (15,self.f_tipo),(1,urwid.Text('|')),
                (15,self.f_marca),
                #
                self.f_cliente
            ]),
            urwid.Columns([
                (9,urwid.Text(' ')),
                #
                (15,self.f_status),(1,urwid.Text('|')),
                (15,self.f_tarefa),
                #
                (15,self.f_dataent),(1,urwid.Text('|')),
                (15,self.f_datasai)
            ]),
            urwid.Divider()
        ])

    def toappend(self):
        return self, None, self._tid

    @staticmethod
    def getHeader():
        return wgtGridRow_oslist(None,cor= ('gridhead', 'head'))
