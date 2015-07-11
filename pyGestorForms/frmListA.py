#!/usr/bin/python
# -*- coding: utf-8 -*-

#
#
import nisk
from nisk import *
import nisk.util
import nisk.widgets
import nisk.TreeList
from nisk.nsatw import *
import thread
from nisk.TUI import *
import nisk.ListBrowser


class frmListAScreens2(nisk.ListBrowser.ListBrowserBase):
    footer_text = [
        ('title', "OK"), ('key', "Enter"), "|",
        ('title', "Voltar"), ('key', "Home"), "|",
        ('title', "Novo"), ('key', "F2"), "|",
        ('title', "Editar"), ('key', "F4"), "|",
        ('title', "Cancelar"), ('key', "ESC" ), "\n",
        #
        # ('title', "Infomacoes"), ('key', "F5"), "|",
        # ('title', "Ajuda"), ('key', "Ctrl-Back"), "|",
    ]

    def __init__(self, params):
        # params['loader'] = self.FoolLoader
        nisk.ListBrowser.ListBrowserBase.__init__(self, params)


    def FoolLoader(self, params):
        rtab = params['rtab']
        ltab = params['ltab']
        search = params['search']
        tree = util.defaultv(params, 'tree', None)
        quantos = util.defaultv(params, 'quantos', 50)

        import pyGestorModel
        from pyGestorModel.orm_listas import grupos, lists_a
        #
        s = pyGestorModel.dbsession.getsession()
        dados = []
        info = {}
        #
        ''''
        def my_import(name):
            mod = __import__(name)
            components = name.split('.')
            for comp in components[1:]:
                mod = getattr(mod, comp)
            return mod'''''
        #
        tabxs = None
        if rtab == 'lists_a':
            tabxs = lists_a
        elif rtab == 'grupos':
            tabxs = grupos
        else:
            return dados

        if tree:
            q = s.query(tabxs).filter(tabxs.tab == ltab, tabxs.nome.like('%' + search + '%'))
        else:
            q = s.query(tabxs).order_by(tabxs.nome).filter(tabxs.tab == ltab)
            if search:
                searchx = search.split(' ')
                for s in searchx:
                    q = q.filter(tabxs.nome.like('%' + s + '%'))
                # q = q.filter(tabxs.nome.like('%' + search + '%'))

        q = q.limit(quantos)
        r = q.all()

        if tree:
            for a in r:
                dados.append({'tid': a.tid, 'id': a.id, 'nome': a.nome, 'pai': a.pai, 'level': a.nivel})
                # dados[a.tid] = {'tid': a.tid, 'dbid': a.id, 'nome': a.nome, 'pai': a.pai, 'level': a.nivel}
        else:
            for a in r:
                dados.append({'tid': a.tid, 'id': a.id, 'nome': a.nome, 'pai': a.tid, 'level': 0})

        return {'dados': dados}



    def callback_acts(self, params={}):
        if util.defaultv(params, 'act', '') == 'add':
            txt = util.defaultv(params, 'nome', '')
            self.set_search(txt)

        if util.defaultv(params, 'act', '') == 'open':
            txt = util.defaultv(params, 'nome', '')
            self.set_search(txt)

    def unhandled_input(self, k):

        if k == "f2":
            self._widgetprocessa(conf.cmds.dlg_frmlistsA_add,
                         {'nome': self.search, 'ltab':self.ltab, 'callback': self.callback_acts})
            return k

        if k == "f4":
            self._widgetprocessa(conf.cmds.dlg_frmlistsA_open,
                         {'id': self.getTid(), 'ltab':self.ltab, 'callback': self.callback_acts})
            return k

        if k == 'home':
            self.r = dlger.back
            self._widgetsession.UnShowWidget()
            return k

        return nisk.ListBrowser.ListBrowserBase.unhandled_input(self, k)


def defaultPopupSelector_(wgtFieldBoxDb1, params=None):

    act = util.defaultv(params, 'act', 'select')

    if act=='select':
        if wgtFieldBoxDb1 is None:
            return
        d, w, r = None, None, None
        tabela = wgtFieldBoxDb1.tabela
        ltabela = wgtFieldBoxDb1.ltabela

        if tabela == 'grupos':
            w = frmListAScreens2({'rtab': tabela, 'ltab': ltabela})
        elif tabela == 'contatos':
            import frmListContatos

            w = frmListContatos.frmListContatos2({})
        else:  # if tabela == 'lists_a':
            w = frmListAScreens2({'rtab': 'lists_a', 'ltab': ltabela})

        if not w is None:
            r, d = w.Show(_widgetpai=wgtFieldBoxDb1)
            if r == dlger.ok:
                wgtFieldBoxDb1.setValue(d['tid'])
        else:
            nisk.util.dump(r, d)

    if act=='edit':
        if wgtFieldBoxDb1 is None:
            return
        d, w, r = None, None, None
        tabela = wgtFieldBoxDb1.tabela
        ltabela = wgtFieldBoxDb1.ltabela

        if tabela == 'grupos':
            w = frmListAScreens2({'rtab': tabela, 'ltab': ltabela})
        elif tabela == 'contatos':
            import frmListContatos

            w = frmListContatos.frmListContatos2({})
        else:  # if tabela == 'lists_a':
            w = frmListAScreens2({'rtab': 'lists_a', 'ltab': ltabela})

        if not w is None:
            r, d = w.Show(_widgetpai=wgtFieldBoxDb1)
            if r == dlger.ok:
                wgtFieldBoxDb1.setValue(d['tid'])
        else:
            nisk.util.dump(r, d)
