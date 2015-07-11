#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging, threading
#
import urwid
#
from urwidtrees.tree import SimpleTree
from urwidtrees.widgets import TreeBox
#
import conf
import nisk
import nisk.util as util
from nisk.dialogs import dlger


class FocusableText(urwid.WidgetWrap):
    """Selectable Text used for nodes in our example"""

    def __init__(self, txt):
        t = urwid.Text(txt)
        w = urwid.AttrMap(t, 'body', 'focus')
        urwid.WidgetWrap.__init__(self, w)
        self.wor

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key


class FocusableRow(urwid.WidgetWrap):
    """Selectable Text used for nodes in our example"""

    def __init__(self, txt):
        t = urwid.Text(util.defiter(txt, 0, ''))
        t.wrap
        t2 = urwid.Text(str(util.defiter(txt, 1, '')))
        t.set_wrap_mode('clip')
        t2.set_wrap_mode('clip')
        c = urwid.Columns([('weight', 8, t), ('weight', 2, t2)], dividechars=1)
        # c = urwid.Columns([( 28, t), ( 12, t2)])
        w = urwid.AttrMap(c, 'body', 'focus')
        urwid.WidgetWrap.__init__(self, w)

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key


class TreeBoxx(TreeBox):
    def render(self, size, focus):
        # logging.debug('render size1:'+str(size))
        r = TreeBox.render(self, size, focus)
        # try:
        # logging.debug('render canvas r:'+str(r.rows()))
        # except:
        # logging.debug('render canvas r error')
        # pass
        # try:
        # logging.debug('render canvas c:'+str(r.cols()))
        # except:
        # logging.debug('render canvas c error')
        # pass
        return r


class ListBrowserBase(dlger):
    footer_text = [
        ('title', "OK"), ('key', "Enter"), "|",
        ('title', "Cancelar"), ('key', "ESC" ),
    ]

    txt_noresults = '-- sem resultados --'
    txt_listbox_nulo = '-- Nulo --'
    txt_typetosearch = '...Digite para pesquisar...'

    def __init__(self, params):
        self._params = params

        self.header = urwid.Text(self.txt_typetosearch)

        self.rtab = util.defaultv(params, 'rtab', None)
        self.rtab_orm = util.defaultv(params, 'rtab_orm', None)
        self.ltab = util.defaultv(params, 'ltab', None)
        self.search = util.defaultv(params, 'search', '')
        self.loader = util.defaultv(params, 'loader', self.FoolLoader)
        self.tree = False

        self.fn = [(urwid.Text(self.txt_noresults), [])]
        self.tw = SimpleTree(self.fn)
        self.listbox = TreeBoxx(self.tw)

        self.listbox.offset_rows = 3

        self._footertxb = urwid.Text(self.footer_text)
        self.footer = urwid.AttrWrap(self._footertxb, 'foot')

        self.view = urwid.Frame(
            urwid.AttrWrap(self.listbox, 'body'),
            header=urwid.AttrWrap(self.header, 'head'),
            footer=self.footer, focus_part='body')

        dlger.__init__(self)

    def FoolLoader(self, params):

        retorno = {'dados': {}, 'info': {}}
        # dados[a.tid] = {'tid': a.tid, 'dbid': a.id, 'nome': a.nome, 'pai': a.tid, 'level': 0}

        logging.debug(':(')
        return retorno


    def load(self):

        # pprint(self.listbox)
        # pprint(vars(self.listbox))
        # print(dir(self.listbox))
        # self.params['quantos'] = self.listbox.

        self._params['search'] = self.search
        consulta = self.loader(self._params)
        needresort = util.defaultv(consulta, 'needresort', False)

        del self.fn[:]
        self.fn.append((urwid.Text(":"), None))

        if needresort:
            dadosx = util.defaultv(consulta, 'dados', {})
            nomes = {}

            for x in dadosx.values():
                nomes[x['nome'].lower()] = x['tid']
            namex = sorted(nomes)

            for x in namex:
                self.fn.append((FocusableRow(dadosx[nomes[x]]['nome']), None))
        else:
            dados = util.defaultv(consulta, 'dados', [])
            for x in dados:
                self.fn.append((FocusableRow([x['nome'], str(x['tid'])]), None, x['tid']))
            try:
                pass
            except:
                logging.error('erro ListBrowserBase.load')

        if len(self.fn) == 0:
            self.fn.append((urwid.Text(self.txt_noresults), None))

        self.listbox.refresh()
        # self.listbox.focus_first_child()


    def update(self, txtbox, changedtext):
        set_search(changedtext)

    def set_search(self, txt):
        self.search = txt

        self.header.set_text(
            'pesquisa: %s' % self.search if len(self.search) > 0
            else self.txt_typetosearch)

        self.load()

    def unhandled_input(self, k):
        # logging.debug('lst ' + str(k))
        if len(k) == 1:
            txt = self.search + k
            self.set_search(txt)
            return True

        elif k == "backspace":
            txt = self.search[:-1]
            self.set_search(txt)
            return True

        elif k == "esc":
            self.r = dlger.cancel
            self._widgetsession.UnShowWidget()
            return True

        elif (k == 'enter'):
            x = self.getTid()
            if x:
                self.r = dlger.ok
                self._widgetsession.UnShowWidget()
                return True
            else:
                util.show('É necessário selecionar um registro para prosseguir!')
                return True
                pass

        return nisk.dialogs.dlger.unhandled_input(self, k)

    def getTid(self):
        try:
            x = self.listbox.get_focus()
            # util.dump(x)
            # f = x[1][0]
            x = self.rdata['tid'] = self.fn[x[1][0]][2]
            return x
        except:
            return None

    def Show(self, _widgetpai, isdialog=True):
        self._widgetregistrapai(_widgetpai)

        bodyWithInfo = self.view
        headBodyFootFrame = nisk.widgets.LineBox(bodyWithInfo, title='|** Selecionar **|')

        bkg = urwid.AttrWrap(headBodyFootFrame, 'PopupMessageBg')

        sx = conf.sizes['ListBrowser1']
        over = urwid.Overlay(bkg, self._widgetsession.mainframe.body, sx[0], sx[1], sx[2], sx[3])

        self.load()
        # self._widgetonshow()
        if isdialog:
            lck = threading.Lock()
            self._widgetsession.ShowDialogWidget(over, self.unhandled_input, lck, _nestedwidget=self)
            nisk.util.espera(lck)
        else:
            self._widgetsession.ShowDialogWidget(over, self.unhandled_input, _nestedwidget=self, isDialog=False)

        return self.r, self.rdata
