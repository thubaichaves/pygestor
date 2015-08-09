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
import nisk.dialogs


class FocusableText(urwid.WidgetWrap):
    """Selectable Text used for nodes in our example"""

    def __init__(self, txt,cor=None):
        if not cor:
            cor = ('gridrow', 'gridrow_of')
        t = urwid.Text(txt)
        w = urwid.AttrMap(t,cor[0],cor[1])
        urwid.WidgetWrap.__init__(self, w)

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key


class FocusableRow(urwid.WidgetWrap):
    """Selectable Text used for nodes in our example"""

    def __init__(self, txt,cor=None):
        if not cor:
            cor = ('gridrow', 'gridrow_of')
        t = urwid.Text(util.defiter(txt, 0, ''))
        t2 = urwid.Text(str(util.defiter(txt, 1, '')))
        t.set_wrap_mode('clip')
        t2.set_wrap_mode('clip')
        c = urwid.Columns([('weight', 8, t), ('weight', 2, t2)], dividechars=1)
        # c = urwid.Columns([( 28, t), ( 12, t2)])
        w = urwid.AttrMap(c,cor[0],cor[1])
        urwid.WidgetWrap.__init__(self, w)

    def selectable(self):
        return True

    def keypress(self, size, key):
        return key


class Edit_searchfield(urwid.Edit):

    def selectable(self): return False

    def __init__(self, *arg,**kw):
        super(self.__class__,self).__init__(*arg,**kw)

        
class TreeBoxx(TreeBox):
    def render(self, size, focus):
        # logging.debug('render size1:'+str(size))
        r = TreeBox.render(self, size, focus)
        self._size = size
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
        ('title', "Cancelar"), ('key', "ESC"),
    ]

    txt_noresults = '-- sem resultados --'
    txt_listbox_nulo = '-- Nulo --'
    txt_typetosearch = '...Digite para pesquisar: '

    def __init__(self, params):
        self._params = params

        self.header = Edit_searchfield(self.txt_typetosearch)
        urwid.connect_signal(self.header, 'change', self._searchfield_changed)

        self.rtab = util.defaultv(params, 'rtab', None)
        self.rtab_orm = util.defaultv(params, 'rtab_orm', None)
        self.ltab = util.defaultv(params, 'ltab', None)
        self.search = util.defaultv(params, 'search', '')
        self.loader = util.defaultv(params, 'loader', self.FoolLoader)
        self.tocall = util.defaultv(params, 'tocall', None)
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

        self.listbox.keypress=self.listkeypress
        # self.header.keypress=self.editkeypress
        self._dirty = False

        dlger.__init__(self)

    def _setdirty(self):
        if not self._dirty:
            self.clear()
        self._dirty=True

    def _unsetdirty(self):
        self._dirty=False

    def _alarmcallback(self):
        self._unsetdirty()
        self.load()

    def set_search(self, txt, remostra=True):
        dirty = self.search != txt
        self.search = txt
        if remostra:
            self.header.set_edit_text( self.search)

        if dirty:
            self._setdirty()

    def _searchfield_changed(self,a=None,b=None, *arg):
        self.set_search(b,remostra=False)


    def FoolLoader(self, params):

        retorno = {'dados': {}, 'info': {}}
        # dados[a.tid] = {'tid': a.tid, 'dbid': a.id, 'nome': a.nome, 'pai': a.tid, 'level': 0}

        logging.debug(':(')
        return retorno

    def listkeypress(self, size, key):
        if len(key) == 1 or\
            key in ('backspace','delete'):
                urwid.Edit.keypress(self.header,(size[0],),key)
                return 'up'
        return TreeBoxx.keypress(self.listbox,size,key)

    def editkeypress(self, size, key):
        if key in ('down', 'enter','tab'):
            return TreeBoxx.keypress(self.listbox,self.listbox._size,key)
        return urwid.Edit.keypress(self.header,size,key)

    def load(self):
        self._params['search'] = self.search
        if self.listbox._size:
            self._params['quantos']= self.listbox._size[1]
        consulta = self.loader(self._params)
        needresort = util.defaultv(consulta, 'needresort', False)

        del self.fn[:]
        self.fn.append((urwid.Text("."), None))
        self.fn.append((urwid.Text("."), None))
        self.fn.append((urwid.Text("."), None))

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
            inv=0
            for x in dados:
                cor = ('gridrow','gridrow_of') if inv % 2 else('gridrowb','gridrow_of')
                inv=inv+2
                self.fn.append((FocusableRow([x['nome'], str(x['tid'])]
                                             ,cor=cor), None, x['tid']))
                self.fn.append((urwid.AttrWrap( urwid.Text(''),'gridrowb','gridrow_of'), None))

            try:
                pass
            except:
                logging.error('erro ListBrowserBase.load')

        if len(self.fn) == 0:
            self.fn.append((urwid.Text(self.txt_noresults), None))

        self.listbox.refresh()
        # self.listbox.focus_first_child()
        self._unsetdirty()

    def clear(self):
        del self.fn[:]
        self.fn.append((urwid.Text(" "), None))
        self.fn.append((urwid.Text(" "), None))
        self.fn.append((urwid.Text(" "), None))
        self.fn.append((urwid.Text(" "), None))
        self.fn.append((urwid.Edit("   Pressione TAB para Pesquisar  "), None))

        self.listbox.refresh()
        # self.listbox.focus_first_child()

    def _widgetonshow(self):
        dlger._widgetonshow(self)

    def _widgetonunshow(self):
        dlger._widgetonunshow(self)
        if self.tocall:
            self.tocall((self.r, self.rdata, self._params))

    def update(self, txtbox, changedtext):
        self.set_search(changedtext)

    def unhandled_input(self, k):
        # logging.debug('lst ' + str(k))
        if len(k) == 1:
            #txt = self.search + k
            #self.set_search(txt)
            return True

        elif k == "esc":
            self.r = dlger.cancel
            self._widgetsession.UnShowWidget()
            return True

        elif k == "tab":
            self.load()
            return True

        elif (k == 'enter'):
            x = self.getTid()
            if x:
                self.r = dlger.ok
                self._widgetsession.UnShowWidget()
                return True
            else:
                nisk.dialogs.GenericDialogx.dialog_ShowText(
                    'É necessário selecionar um registro para prosseguir!', self)
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

    def Show(self, _widgetpai, isdialog=False, tocall=None):
        self._widgetregistrapai(_widgetpai)

        if tocall:
            self.tocall = tocall

        bodyWithInfo = self.view
        headBodyFootFrame = nisk.widgets.LineBox(bodyWithInfo, title='|** Selecionar **|')

        bkg = urwid.AttrWrap(headBodyFootFrame, 'PopupMessageBg')

        # sx = conf.sizes['ListBrowser1']
        # over = urwid.Overlay(bkg, self._widgetsession.mainframe.body, sx[0], sx[1], sx[2], sx[3])
        # over = urwid.Overlay(over, self._widgetsession. mainframe.body,('fixed left', 8 ), sx[1], sx[2], sx[3])
        over = bkg

        self.load()
        #
        if isdialog:
            lck = threading.Lock()
            self._widgetsession.ShowDialogWidget(over, self.unhandled_input, lck, _nestedwidget=self)
            nisk.util.espera(lck)
            return self.r, self.rdata
        else:
            self._widgetsession.ShowDialogWidget(over, self.unhandled_input, None, _nestedwidget=self, isDialog=False)

