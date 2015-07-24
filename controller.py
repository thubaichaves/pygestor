#!/usr/bin/python
# -- coding: utf-8 --

import puremvc.patterns.facade
# import controller, components
import puremvc.patterns.command
import puremvc.interfaces
# import model, view, main
# import puremvc.interfaces
import puremvc.patterns.mediator

import thread
import logging
import urwid
import nisk
import nisk.TUI
import nisk.util
import nisk.widgets
import nisk.dialogs
import nisk.formmer
import crtl_os
import crtl_contatos
import crtl_listas
import conf
import pyGestorForms
import pyGestorModel.proxies
import pyGestorForms.frmListContatos
import pyGestorForms.frmLogin


class pyGestorFacade(puremvc.patterns.facade.Facade, nisk.TUI.nestedwidget):
    fac = None
    mdi = None

    _cmdlist = []

    def __init__(self):
        self.initializeFacade()
        self._sessionnumber = None
        self._sessiontui = None

    @staticmethod
    def getInstance():
        pyGestorFacade.fac = pyGestorFacade()
        return pyGestorFacade.fac

    @staticmethod
    def mainInstance():
        if pyGestorFacade.fac is None:
            pyGestorFacade.fac = pyGestorFacade()
        return pyGestorFacade.fac

    def initializeFacade(self):
        super(pyGestorFacade, self).initializeFacade()

        self.initializeController()

    def initializeController(self):
        pyGestorFacade._cmdlist = [
            (conf.cmds.cmd_frmMain, pyGestorFacade._cmd_frmMain),
            (conf.cmds.STARTUP, pyGestorFacade.StartupCommand),
            (conf.cmds.OS_OPEN, pyGestorFacade._OS_OPEN),
            (conf.cmds.OS_ADD, pyGestorFacade._OS_ADD),
            (conf.cmds.OS_ADD, pyGestorFacade._OS_ADD),
            (conf.cmds.OS_ADD, pyGestorFacade._OS_ADD),
            (conf.cmds.cmd_checkLogin, pyGestorFacade._cmd_checkLogin),
            (conf.cmds.cmd_os_impr, pyGestorFacade._cmd_os_impr),
            (conf.cmds.cmd_os_create, pyGestorFacade._cmd_os_create),
            (conf.cmds.dlg_frmlistcontatos_add, pyGestorFacade._dlg_frmlistcontatos_add),
            (conf.cmds.dlg_frmlistcontatos_open, pyGestorFacade._dlg_frmlistcontatos_open),
            (conf.cmds.dlg_frmlistsA_add, pyGestorFacade._dlg_frmlistsA_add),
            (conf.cmds.dlg_frmlistsA_open, pyGestorFacade._dlg_frmlistsA_open),
        ]
        super(pyGestorFacade, self).initializeController()

        for (x, y) in pyGestorFacade._cmdlist:
            super(pyGestorFacade, self).registerCommand(x, y)

            # super(pyGestorFacade, self).registerCommand(AppFacade.DELETE_USER, DeleteUserCommand)
            # super(pyGestorFacade, self).registerCommand(AppFacade.ADD_ROLE_RESULT, AddRoleResultCommand)

    def _widgetprocessa(self, mensagem, dados=None, origem=None):
        # nisk.util.dump([mensagem,dados,origem])
        return self.sendNotification(mensagem, dados)

    def sendNotification(self, notificationName, body=None, noteType=None):
        self.notifyObservers(
            pyGestorFacade.superNotification(notificationName, body, noteType, self))

    # controller
    class StartupCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
        def execute(self, note):
            self.facade.registerProxy(pyGestorModel.proxies.OS_Proxy())
            self.facade.registerProxy(pyGestorModel.proxies.RoleProxy())

            self._sessiontui = note.getBody()
            self.facade.registerMediator(pyGestorFacade.NewOSMediator(1))
            self.facade.registerMediator(pyGestorFacade.DialogMediator(2))
            self.facade.registerMediator(pyGestorFacade.statusbar_Mediator(2))
            # self.facade.registerMediator(Mediator_OSCreate())

            # self.facade.registerMediator(view.UserFormMediator(mainPanel.userForm))
            # self.facade.registerMediator(view.UserListMediator(mainPanel.userList))
            # self.facade.registerMediator(view.RolePanelMediator(mainPanel.rolePanel))

    class superNotification(puremvc.patterns.observer.Notification):
        def __init__(self, name, body=None, noteType=None, facade=None):
            super(pyGestorFacade.superNotification, self).__init__(name, body, noteType)
            self.facade = facade

    class _OS_PRINTENT(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
        def execute(self, note):
            facade = note.facade if issubclass(type(note), pyGestorFacade.superNotification) else None
            thread.start_new(crtl_os.crtl_os.actImprimeOS, (facade,))

    class _cmd_os_impr(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
        def execute(self, note):
            facade = note.facade if issubclass(type(note), pyGestorFacade.superNotification) else None

            b = note.getBody()
            thread.start_new(crtl_os.crtl_os.actImprimeOS, (facade, b))

    class _cmd_os_create(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
        def execute(self, note):
            facade = note.facade if issubclass(type(note), pyGestorFacade.superNotification) else None

            b = note.getBody()
            #thread.start_new(crtl_os.crtl_os.actImprimeOS, (facade, b))
            x = crtl_os.crtl_os.os_new(facade)
            x.act_start()

    class _cmd_frmMain(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
        def execute(self, note):
            backref = note.getBody()

            facade = note.facade if issubclass(type(note), pyGestorFacade.superNotification) else None

            if backref == 'os_abrir':
                pyGestorFacade.mainInstance().sendNotification(conf.cmds.OS_OPEN, '')
                pyGestorFacade.mainInstance().sendNotification(conf.cmds.SESSION_UNLOGIN, '')
                #
            elif backref == 'os_nova':
                pyGestorFacade.mainInstance().sendNotification(conf.cmds.OS_ADD, '')#
            elif backref == 'os_create':
                pyGestorFacade.mainInstance().sendNotification(conf.cmds.cmd_os_create, '')
                #
            elif backref == 'os_print_ent':
                pyGestorFacade.mainInstance().sendNotification(conf.cmds.OS_PRINTENT, '')
                #
            elif backref == 'sair':
                nisk.tui.mdi.stop()
                #
            elif backref == 'logout':
                facade._widgetprocessa(conf.cmds.cmd_checkLogin)
                #
            else:
                nisk.dialogs.GenericDialogx.dialog_ShowText('Não Identificado: ' + str(backref), self)
                pass

    class _cmd_checkLogin(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
        def execute(self, note):
            backref = note.getBody()

            facade = note.facade if issubclass(type(note), pyGestorFacade.superNotification) else None

            f = pyGestorForms.frmLogin.frmLoginA(facade)
            # thread.start_new(f.show, ())
            f.show()

    class _dlg_frmlistcontatos_add(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
        def execute(self, note):
            b = note.getBody()

            facade = note.facade if issubclass(type(note), pyGestorFacade.superNotification) else None

            f = crtl_contatos.contatos_new(facade, b)
            f.act_start()

    class _dlg_frmlistcontatos_open(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
        def execute(self, note):
            b = note.getBody()

            facade = note.facade if issubclass(type(note), pyGestorFacade.superNotification) else None

            f = crtl_contatos.contatos_open(facade, b)
            f.act_start()




    class _dlg_frmlistsA_add(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
        def execute(self, note):
            b = note.getBody()

            facade = note.facade if issubclass(type(note), pyGestorFacade.superNotification) else None

            f = crtl_listas.listsA_new(facade, b)
            f.act_start()

    class _dlg_frmlistsA_open(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
        def execute(self, note):
            b = note.getBody()

            facade = note.facade if issubclass(type(note), pyGestorFacade.superNotification) else None

            f = crtl_listas.listsA_open(facade, b)
            f.act_start()

    class _OS_ADD(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
        def execute(self, note):
            facade = note.facade if issubclass(type(note), pyGestorFacade.superNotification) else None
            x = crtl_os.crtl_os.os_new(facade)
            x.act_start()

    class _OS_OPEN(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
        def execute(self, note):
            noteName = note.getName()
            noteBody = note.getBody()
            facade = note.facade if issubclass(type(note), pyGestorFacade.superNotification) else None

            x = crtl_os.crtl_os.os_open(facade)
            x.act_start()

    # view
    class DialogMediator(puremvc.patterns.mediator.Mediator, puremvc.interfaces.IMediator):
        NAME = 'DialogMediator'

        def __init__(self, viewComponent):
            super(pyGestorFacade.DialogMediator, self).__init__(pyGestorFacade.DialogMediator.NAME, viewComponent)

        def listNotificationInterests(self):
            return [
                conf.cmds.SHOW_DIALOG,
                conf.cmds.SESSION_UNLOGIN
            ]

        def handleNotification(self, note):
            noteName = note.getName()
            if noteName == conf.cmds.SHOW_DIALOG:
                logging.debug("SESSION_UNLOGIN - NewOS")

            if noteName == conf.cmds.SESSION_UNLOGIN:
                logging.debug("SESSION_UNLOGIN - Dialog")

    class NewOSMediator(puremvc.patterns.mediator.Mediator, puremvc.interfaces.IMediator):
        NAME = 'NewOSMediator'

        def __init__(self, viewComponent):
            super(pyGestorFacade.NewOSMediator, self).__init__(pyGestorFacade.NewOSMediator.NAME, viewComponent=None)

        def listNotificationInterests(self):
            return [
                # pyGestorFacade.OS_ADD,
                conf.cmds.SESSION_UNLOGIN
            ]

        def handleNotification(self, note):
            noteName = note.getName()
            if noteName == conf.cmds.OS_ADD:
                logging.debug("SESSION_UNLOGIN - NewOS")

            if noteName == conf.cmds.SESSION_UNLOGIN:
                logging.debug("SESSION_UNLOGIN - NewOS")

    class statusbar_Mediator(puremvc.patterns.mediator.Mediator, puremvc.interfaces.IMediator):

        NAME = 'statusbar_Mediator'

        def __init__(self, viewComponent):
            super(pyGestorFacade.statusbar_Mediator, self).__init__(pyGestorFacade.statusbar_Mediator.NAME,
                                                                    viewComponent=None)

        def listNotificationInterests(self):
            return [
                conf.cmds.dlg_statusbar_pop,
                conf.cmds.dlg_statusbar_put,
                conf.cmds.dlg_statusbar_change,
            ]

        def handleNotification(self, note):
            noteName = note.getName()
            noteBody = note.getBody()
            # nisk.util.dump((noteBody, noteName))

            if noteName == conf.cmds.dlg_statusbar_put:
                try:
                    facade = note.facade if isinstance(note, pyGestorFacade.superNotification) else None
                    if facade:
                        facade._widgetgetsession().mainframe.footer.putInfo(noteBody)
                except:
                    pass

            if noteName == conf.cmds.dlg_statusbar_pop:
                try:
                    facade = note.facade if isinstance(note, pyGestorFacade.superNotification) else None
                    if facade:
                        facade._widgetgetsession().mainframe.footer.popInfo()
                except:
                    pass

            if noteName == conf.cmds.dlg_statusbar_change:
                try:
                    facade = note.facade if isinstance(note, pyGestorFacade.superNotification) else None
                    if facade:
                        facade._widgetgetsession().mainframe.footer.changeInfo(noteBody)
                except:
                    pass
