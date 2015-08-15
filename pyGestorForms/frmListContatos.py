#!/usr/bin/python
# -*- coding: utf-8 -*-

import nisk
import app
import nisk.TUI
import conf
from nisk.ListBrowser import ListBrowserBase
import nisk.widgets
import nisk.dialogs
import nisk.util as util
import nisk.TreeList
import pyGestorModel
from pyGestorModel.orm_contatos import contatos


class frmListContatos2(ListBrowserBase):
    footer_text = []

    def __init__(self, params):
        self.footer_text = conf.footer_frmListContatos2
        ListBrowserBase.__init__(self, params)

    def FoolLoader(self, params):
        search = util.defaultv(params, 'search', '')
        quantos = util.defaultv(params, 'quantos', 50)

        #
        s = pyGestorModel.dbsession.getsession()
        dados = []
        info = {}

        q = s.query(contatos).order_by(contatos.nome).filter(contatos.exc != 1)

        search = util.asUnicode(search)

        if len(search) > 0:
            searchx = search.split(' ')
            for s in searchx:
                q = q.filter(contatos.nome.like('%' + s + '%'))

        q = q.limit(quantos)

        # nisk.util.dump(q)
        r = q.all()

        for a in r:
            dados.append({'tid': a.id, 'id': a.id, 'nome': a.nome, 't4a': a.t4a})
            # dados[a.tid] = {'tid': a.tid, 'dbid': a.id, 'nome': a.nome, 'pai': a.pai, 'level': a.nivel}

        return {'dados': dados}

    def callback_acts(self, params={}):
        if util.defaultv(params, 'act', '') == 'add':
            if util.defaultv(self._params, 'onNew_callback_parent', False):
                self.r = nisk.dialogs.dlger.ok
                self.rdata['tid'] = util.defaultv(params, 'id', '')
                self._widgetsession.UnShowWidget()
            else:
                txt = util.defaultv(params, 'nome', '')
                self.set_search(txt)

        if util.defaultv(params, 'act', '') == 'open':
            txt = util.defaultv(params, 'nome', '')
            self.set_search(txt)

    def _widgetonshow(self):
        ListBrowserBase._widgetonshow(self)
        self._widgetprocessa('dlg_statusbar_put', "Selecione o Cliente Para a Nova OS", self)

    def _widgetonunshow(self):
        ListBrowserBase._widgetonunshow(self)
        self._widgetprocessa('dlg_statusbar_pop')

    def unhandled_input(self, k):

        if k == "f2":
            self._widgetprocessa(conf.cmds.dlg_frmlistcontatos_add,
                         {'nome': self.search, 'callback': self.callback_acts})
            return k

        if k == "f4":
            self._widgetprocessa(conf.cmds.dlg_frmlistcontatos_open,
                         {'id': self.getTid(), 'callback': self.callback_acts})
            return "x"

        if (k == 'home'):  # "crtl _" = backspace
            self.r = nisk.dialogs.dlger.back
            self._widgetsession.UnShowWidget()
            return k
        return ListBrowserBase.unhandled_input(self, k)

# class frmListContatos(nisk.TreeList.TreeListBrowserBase):
#     def __init__(self, params={}):
#         nisk.TreeList.TreeListBrowserBase.__init__(self, loader=self.loader_contatos)
#
#
#         # urwid.connect_signal(self.header, "change", self.update)
#
#     def loader_contatos(self, params={}):
#         quantos = util.defaultv(params, 'quantos', 50)
#         search = util.defaultv(params, 'search', '')
#         #
#         import pyGestorModel
#         from pyGestorModel.orm_contatos import contatos
#         #
#         s = pyGestorModel.dbsession.getsession()
#         dados = {}
#         info = {}
#         #
#         q = s.query(contatos)
#         #
#         search = search.split(' ')
#         for ss in search:
#             q = q.filter(contatos.nome.like('%' + ss + '%'))
#         #
#         q = q.order_by(contatos.nome).limit(quantos)
#         #
#         info['totalcount'] = q.count()
#         r = q.all()
#         for a in r:
#             dados[a.id] = {'tid': a.id, 'dbid': a.id, 'nome': a.nome, 'pai': a.id, 'level': 0}
#
#         return dados, info
