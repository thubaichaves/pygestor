#!/usr/bin/python
# -*- coding: utf-8 -*-

from nisk import *
from nisk.nsatw import *
from nisk.formmer import tfld
import nisk.dialogs
# import nisk.util as util

import imprimir
import urwid
#
# import puremvc.patterns.facade
# import puremvc.patterns.command
# import puremvc.interfaces
import puremvc.patterns.mediator
import pyGestorModel
import conf
import app

from nisk.TUI import nestedwidget
import pyGestorForms.frmListContatos
from pyGestorForms import frmListA


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

        if util.isInt(osn):
            osn = int(osn)
            imprimir.Imprimir_EntradaOS(osn)
        else:
            nisk.dialogs.dlgInput.show('OS Inexistente', _widgetpai)

    @staticmethod
    def actOSNew(_widgetpai):
        util.TerminalLogger.setup()

        # log.debug('passou1')
        try:
            import pyGestorForms.frmListContatos
            from pyGestorForms import frmListA
        except Exception, e:
            log.exception(e)
        # todo: erro ao usar python run.py
        # log.debug('passou2')

        scancela = step = 0
        scliente = step = step + 1
        stipo = step = step + 1
        smarca = step = step + 1
        sresp = step = step + 1
        sfim = step = step + 1
        #
        step = scliente
        r, s = None, None
        dados = {}

        while step not in (scancela, sfim):
            if step == scliente:
                frmc = pyGestorForms.frmListContatos.frmListContatos2({})
                r, dados['cliente'] = frmc.Show(_widgetpai=_widgetpai)
            if step == stipo:
                w = frmListA.frmListAScreens2({'rtab': 'lists_a', 'ltab': 'ostip'})
                r, dados['tipo'] = w.Show(_widgetpai=_widgetpai)
            if step == smarca:
                w = frmListA.frmListAScreens2({'rtab': 'lists_a', 'ltab': 'osfab'})
                r, dados['marca'] = w.Show(_widgetpai=_widgetpai)
            if step == sresp:
                w = frmListA.frmListAScreens2({'rtab': 'lists_a', 'ltab': 'sysus'})
                r, dados['usrresp'] = w.Show(_widgetpai=_widgetpai)
            # log.debug('step:' + str(step))
            if r == dlger.ok:
                step = step + 1
            elif r == dlger.back:
                step -= 1
            elif r == dlger.cancel:
                step = scancela
            if step == sfim:
                pass
            if step == scancela:
                return

        w = formmer_os_new(params={'new': True, 'dados': dados}, dados=dados)
        w._widgetregistrapai(_widgetpai)
        w.show()

        try:
            pass
        except Exception, e:
            logging.exception(e)

        pass

    class os_new(nestedwidget):
        def __init__(self, _widgetpai):
            crtl_os.os_new.scancela = step = 0
            crtl_os.os_new.scliente = step = step + 1
            crtl_os.os_new.stipo = step = step + 1
            crtl_os.os_new.smarca = step = step + 1
            crtl_os.os_new.sresp = step = step + 1
            crtl_os.os_new.sfim = step = step + 1
            #
            self.step = crtl_os.os_new.scliente
            self.r, self.s = None, None
            self.dados = {}

            nestedwidget.__init__(self, _widgetpai)

        def callback(self, data=None):

            if self.step == crtl_os.os_new.scliente:
                (self.r, self.dados['cliente']) = data
            if self.step == crtl_os.os_new.stipo:
                (self.r, self.dados['tipo']) = data
            if self.step == crtl_os.os_new.smarca:
                (self.r, self.dados['marca']) = data
            if self.step == crtl_os.os_new.sresp:
                (self.r, self.dados['usrresp']) = data

            if self.r == dlger.ok:
                self.step = self.step + 1
            elif self.r == dlger.back:
                self.step -= 1
            elif self.r == dlger.cancel:
                self.step = crtl_os.os_new.scancela

            self.step_x(self.step)

        def step_x(self, step, data=None):
            if step == crtl_os.os_new.scliente:
                frmc = pyGestorForms.frmListContatos.frmListContatos2({})
                self.r, self.dados['cliente'] = frmc.Show(_widgetpai=self._widgetpai, isdialog=False, tocall=self.callback)
            if step == crtl_os.os_new.stipo:
                w = frmListA.frmListAScreens2({'rtab': 'lists_a', 'ltab': 'ostip'})
                self.r, self.dados['tipo'] = w.Show(_widgetpai=self._widgetpai, isdialog=False, tocall=self.callback)
            if step == crtl_os.os_new.smarca:
                w = frmListA.frmListAScreens2({'rtab': 'lists_a', 'ltab': 'osfab'})
                self.r, self.dados['marca'] = w.Show(_widgetpai=self._widgetpai, isdialog=False, tocall=self.callback)
            if step == crtl_os.os_new.sresp:
                w = frmListA.frmListAScreens2({'rtab': 'lists_a', 'ltab': 'sysus'})
                self.r, self.dados['usrresp'] = w.Show(_widgetpai=self._widgetpai, isdialog=False, tocall=self.callback)

            if step == crtl_os.os_new.sfim:
                w = formmer_os_new(params={'new': True, 'dados': self.dados}, dados=self.dados)
                w._widgetregistrapai(self._widgetpai)
                w.show(isdialog=False)

            if step == crtl_os.os_new.scancela:
                self._widgetsession.UnShowWidget()

        # def act_fim(self):
        #
        # def act_cancela(self):
        #     pass

        def act_start(self):
            self.step_x(self.step)

    @staticmethod
    def actOSOpen(_widgetpai):
        util.TerminalLogger.setup()

        osn, rr = nisk.dialogs.dlgInput.show('Abrir OS', _widgetpai)

        w = formmer_os_edit(params={'os': util.asInt(osn)})
        w._widgetregistrapai(_widgetpai)
        w.show()

        try:
            pass
        except Exception, e:
            logging.exception(e)

        pass


class formmer_os_new(formmer.formmer):
    footer_text = [
        [('title', "OK"), ('key', "Enter")], "|",
        [('title', "Cancelar"), ('key', "ESC")],
    ]

    text_button_list = [
        [('title', "OK"), ('key', "Enter")],
        ('key', ['C', ('title', "ancelar"), "ESC"]),
        ('key', ['M', ('title', "emu"), "F1"])]

    def __init__(self, params={}, dados={}):
        self.params = params
        self.dados = dados
        self.cc = nisk.widgets.HMenu(conf.menu_os_add, None, defaultcb=self.callbacks, width=24, selfclose=True)

        formmer.formmer.__init__(self, [
            (tfld.itextbox, 'OS', 'os'),
            (tfld.fieldbox, 'Tipo de Equip.', 'tipo', {'ltab': 'ostip'}),
            (tfld.fieldbox, 'Marca', 'marca', {'ltab': 'osfab'}),
            (tfld.textbox, 'Modelo', 'modelo'),
            (tfld.textbox, 'N° Série', 'ns'),
            (tfld.fieldbox, 'Técnico Resp.', 'usrresp', {'ltab': 'sysus'}),
            (tfld.fieldbox, 'Cliente', 'cliente', {'tab': 'contatos'}),
            (tfld.datepicker, 'Data de Entrada', 'dataent',),
            (tfld.textbox, 'Solicitação', 'solicita'),
            (tfld.textbox, 'Acessórios', 'acess'),
            (tfld.textbox, 'Lembrete', 'lembrete'),
            (tfld.textbox, 'Estado de Conservação', 'conserva'),
            (tfld.textbox, 'Sintomas', 'sintoma'),
            (tfld.textbox, 'Observações Internas', 'obsint'),
            (tfld.textbox, 'Observações Impressas', 'obsos'),
            (tfld.fieldbox, 'Status', 'status', {'ltab': 'osstt'}),
            (tfld.fieldbox, 'Tarefa', 'ntarefa', {'ltab': 'osnxt'}),
        ])
        self.binder = mediator_os(self)

    def callbacks(self, backref):
        if backref in ('concluir', 'f6'):
            self.binder.handleCommand('concluir')
            return True
        elif backref in ('cancelar',):
            self.binder.handleCommand('cancelar', )
            return True
        else:
            # tui.mdi.ShowDialogText('Não Identificado: ' + str(backref))
            logging.debug('Não Identificado: ' + str(backref))
            pass
        return False

    def unhandled_input(self, k):
        if k in ('esc',):
            if self.binder.get_isdirty():
                pass
                return True

        if k in ('f1', 'meta m'):
            self.cc.onmenuopen()
            return True

        if k in ('f6',):
            return True

        return self.callbacks(k)
        return False

    def button_press(self, *args):
        pass

    def get_frame(self):

        bkg = widgets.SBListBox(self, (u"\u2593", "handle"), (u"\u2592", "scrollbar_bg"))
        bkg = urwid.AttrWrap(bkg, 'body')
        self._footertxb = urwid.Text(self.footer_text)
        self.footer = urwid.AttrWrap(self._footertxb, 'foot')
        fw = urwid.Frame(bkg)
        fw.set_footer = self.footer
        mt = TabsContainer()

        buttonbar = urwid.GridFlow([urwid.AttrWrap(
            CustomButton(txt, self.button_press, left_border=('scrollbar_bg', "|"), right_border=' '),
            'buttn', 'buttnf') for txt in self.text_button_list],
                                   conf.sizes['statusbarbuttonA'], 0, 0, 'left')

        mt.addTab('Básico', fw)
        mt.addTab('Pagamentos',
                  urwid.Filler(urwid.Text('IMPLANTAR')))

        mt.addComplement(urwid.AttrWrap(buttonbar, 'foot'))
        ff = urwid.AttrWrap(mt, 'body')

        self.cc.setwid(mt)

        lb = urwid.AttrWrap(widgets.LineBox(self.cc, title='Nova OS'), 'windowsborder')
        return lb

    def show(self, isdialog=True):
        x = self.binder.consulta(self.params)
        if x:
            self._widgetsession.ShowDialogWidgetOverlay(self.get_frame(), v_hdlr=self.unhandled_input,
                                                        _nestedwidget=self, isdialog= isdialog)

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
            (tfld.fieldbox, 'Cliente', 'cliente', {'tab': 'contatos'}),
            (tfld.fieldbox, 'Tipo de Equip.', 'tipo', {'ltab': 'ostip'}),
            (tfld.fieldbox, 'Marca', 'marca', {'ltab': 'osfab'}),
            (tfld.textbox, 'Modelo', 'modelo'),
            (tfld.textbox, 'N° Série', 'ns'),
            (tfld.textbox, 'Acessórios', 'acess'),
            (tfld.textbox, 'Estado de Conservação', 'conserva'),
            (tfld.textbox, 'Solicitação', 'solicita'),
            (tfld.textbox, 'Sintomas', 'sintoma'),
            (tfld.textbox, 'Lembrete', 'lembrete'),
            (tfld.fieldbox, 'Técnico Resp.', 'usrresp', {'ltab': 'sysus'}),
            (tfld.textbox, 'Observações Impressas', 'obsos'),
            (tfld.textbox, 'Observações Internas', 'obsint'),
            (tfld.fieldbox, 'Status', 'status', {'ltab': 'osstt'}),
            (tfld.fieldbox, 'Tarefa', 'ntarefa', {'ltab': 'osnxt'}),
            (tfld.datepicker, 'Data de Entrada', 'dataent'),
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
        # fw = widgets.LineBox(self, title='Nova OS')
        # bkg = widgets.SBListBox(self, (u"\u25bc", "handle"), (u"\u25b2", "scrollbar_bg"))
        bkg = widgets.SBListBox(self, (u"\u2593", "handle"), (u"\u2592", "scrollbar_bg"))
        bkg = urwid.AttrWrap(bkg, 'body')
        self._footertxb = urwid.Text(self.footer_text)
        self.footer = urwid.AttrWrap(self._footertxb, 'foot')
        fw = urwid.Frame(bkg)
        fw.set_footer = self.footer
        mt = TabsContainer()

        buttonbar = urwid.GridFlow([urwid.AttrWrap(
            CustomButton(txt, self.button_press, left_border=('scrollbar_bg', "|"), right_border=' '),
            'buttn', 'buttnf') for txt in self.text_button_list],
                                   conf.sizes['statusbarbuttonA'], 0, 0, 'left')

        mt.addTab('Básico', fw)
        mt.addTab('Informações',
                  urwid.Filler(urwid.Text('xxx')))

        # self.menuBar = formmer_os_edit.MainMenux(tui.mdi.loop)
        # self.menuBar =MenuRoller( [('a',MainMenu(tui.mdi.loop)),('b',ProdutosMenu(tui.mdi.loop))])
        # mt.addHeader(   self.menuBar)
        mt.addComplement(urwid.AttrWrap(buttonbar, 'foot'))
        # mt.addFooter(urwid.AttrWrap(urwid.Text('blablabla'), 'foot'))
        ff = urwid.AttrWrap(mt, 'body')

        self.cc.setwid(mt)

        lb = urwid.AttrWrap(widgets.LineBox(self.cc, title='OS'), 'windowsborder')
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
