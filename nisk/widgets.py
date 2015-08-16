#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import logging
import conf
import nisk
import time
import datetime
import util
import nisk.TUI
import nisk.util
from nsatw import *
from urwid import *
import math
import urwid
import wx
import urwidtrees


class NumEdit(Edit):
    """Edit widget for integer values"""

    def valid_char(self, ch):
        """
        Return true for decimal digits.
        """
        return len(ch) == 1 and ch in "0123456789"

    def __init__(self, caption="", default=None):
        """
        caption -- caption markup
        default -- default edit value

        >>> IntEdit(u"", 42)
        <IntEdit selectable flow widget '42' edit_pos=2>
        """
        if default is not None:
            val = str(default)
        else:
            val = ""
        self.__super.__init__(caption, val)

    def keypress(self, size, key):
        """
        Handle editing keystrokes.  Remove leading zeros.

        >>> e, size = IntEdit(u"", 5002), (10,)
        >>> e.keypress(size, 'home')
        >>> e.keypress(size, 'delete')
        >>> print e.edit_text
        002
        >>> e.keypress(size, 'end')
        >>> print e.edit_text
        2
        """
        logging.debug('keypress ' + key)
        (maxcol,) = size
        unhandled = Edit.keypress(self, (maxcol,), key)
        if not unhandled:
            # trim leading zeros
            while self.edit_pos > 0 and self.edit_text[:1] == "0":
                self.set_edit_pos(self.edit_pos - 1)
                self.set_edit_text(self.edit_text[1:])

        return unhandled

    def value(self):
        """
        Return the numeric value of self.edit_text.

        >>> e, size = IntEdit(), (10,)
        >>> e.keypress(size, '5')
        >>> e.keypress(size, '1')
        >>> e.value() == 51
        True
        """
        if self.edit_text:
            return long(self.edit_text)
        else:
            return 0


######################################################################
class wgtIntEdit(urwid.IntEdit):
    signals = ['valuechange', 'focusIn', 'focusOut']

    def __init__(self, caption="", default=None):
        self._lastfocus = False
        self._recem = False
        #self.readonly =readonly
        #if readonly:
        #    defaultx=default if default else ''
        #    urwid.Text.__init__(self,defaultx)
        #else:
        urwid.IntEdit.__init__(self,caption,default)

        self._lastvalue = default
        self._lastlastvalue = default

    def render(self, size, focus=False):
        # if focus != self._lastfocus:
        # # logging.debug('focus ' + str(focus) + ' -> ' +
        # str(self._lastfocus))
        # urwid.emit_signal(self, 'change', self, self.get_text())
        # pass
        (maxcol,) = size
        lastfocus = self._lastfocus
        self._lastfocus = focus
        try:
            # Entra
            if focus and not lastfocus:
                # logging.debug('focus entra ' + str(self.edit_pos) + '/' +
                # str(self.get_edit_text()))
                self._salvalast()
                self._recem = True
                urwid.emit_signal(self, 'focusIn', self, None)
                # maxcol = 1
                # self.set_edit_text('')
            # Sai
            if not focus and lastfocus:
                self._doparse()
                urwid.emit_signal(self, 'valuechange', self, self.value())
                urwid.emit_signal(self, 'focusOut', self, None)
                # logging.debug('focus sai ' + str(self.edit_pos) + '/' +
                # str(self.get_edit_text()))
        except Exception, e:
            logging.exception(e)

        canv = Edit.render(self, (maxcol,), focus=focus)
        # logging.debug('focus conclue ' + str(self.edit_pos) + '/' +
        # str(self.get_edit_text()))
        return canv

    def keypress(self, size, key):
        # logging.debug('keypress ' + key)
        if self._recem and len(key) == 1:
            self._recem = False
            self.set_edit_text('')
        (maxcol,) = size
        unhandled = urwid.IntEdit.keypress(self, (maxcol,), key)
        return unhandled

    def value(self):
        return self._lastvalue

    def _doparse(self):
        self._salvalast()
        self._lastvalue = nisk.util.asInt(self.edit_text)

    def _salvalast(self):
        self._lastlastvalue = self._lastvalue

    def _checamudou(self):
        return self._lastvalue != self._lastlastvalue

    def setvalue(self, v):
        self._lastvalue = v
        self._salvalast()
        t = ''
        if nisk.util.canBeInt(v):
            t = str(v)
        if self.get_edit_text() != t:
            self.set_edit_text(t)


######################################################################
class wgtDateEdit(urwid.IntEdit):
    signals = ['valuechange', 'focusIn', 'focusOut']

    def __init__(self, dformat='%d/%m/%Y %H:%M', default=None,):
        # dformat='dd/mm/yyy HH:MM'
        self._lastfocus = False
        self._lastvalue = None
        self.dformat = dformat
        self._recem = False
        urwid.IntEdit.__init__(self, "", default)
        self._lastvalue = default
        self._lastlastvalue = default

    def valid_char(self, ch):
        return len(ch) == 1 and ch in "0123456789\\/:- "

    def render(self, size, focus=False):
        (maxcol,) = size
        lastfocus = self._lastfocus
        self._lastfocus = focus
        try:
            if focus and not lastfocus:
                self._salvalast()
                self._recem = True
                urwid.emit_signal(self, 'focusIn', self, None)
            if not focus and lastfocus:
                self._doparse()
                urwid.emit_signal(self, 'valuechange', self, self.value())
                urwid.emit_signal(self, 'focusOut', self, None)
        except Exception, e:
            logging.exception(e)
        canv = Edit.render(self, (maxcol,), focus=focus)
        return canv

    def _salvalast(self):
        self._lastlastvalue = self._lastvalue

    def _doparse(self):
        if len(self.get_edit_text()) == 0:
            self._salvalast()
            self._lastvalue = None
        else:
            # nisk.util.dump(self.get_edit_text())
            x = nisk.util.asDateTime(self.get_edit_text())
            # nisk.util.dump([x,self.get_edit_text(),'parse'])
            if not x is None:
                self._salvalast()
                self._lastvalue = x
            self._show()

    def _show(self):
        t = ''
        try:
            t = self._lastvalue.strftime(self.dformat)
        except:
            pass  # if v is datetime.datetime or v is datetime.date or v is time else '-'
        self.set_edit_text(t)

    def _checamudou(self):
        return self._lastvalue != self._lastlastvalue

    def keypress(self, size, key):
        key = self.__super.keypress(size, key)
        if key == "tab":
            return 'down'

        if key == "enter":
            return 'tab'

        elif key == "shift tab":
            return 'up'

        else:
            return key

    def value(self):
        return self._lastvalue

    def setvalue(self, v):
        if v:
            v = v.replace(second=0,microsecond=0)
        self._lastvalue = v
        self._salvalast()
        self._show()


######################################################################
class bindablefield(nisk.TUI.nestedwidget):
    def __init__(self):
        self.bindf = None

        nisk.TUI.nestedwidget.__init__(self)

    def setOnChange(self, cb, sng='change'):
        urwid.connect_signal(self, sng, cb)

    def get_cbdata(self):
        pass

    def set_cbdata(self):
        pass

    def get_bindf(self):
        return self.bindf
        pass

    def set_bindf(self, v):
        self.bindf = v
        pass

    def GetValue(self):
        return None
        #

    def setValue(self, cod):
        pass

    def validate(self):
        pass

    def _widgetinformafilhos(self, mensagem, dados=None, origem=None):
        nisk.TUI.nestedwidget._widgetinformafilhos(self, mensagem, dados, origem)
        if mensagem == 'validate':
            self.validate()


######################################################################
class wgtFieldBox(AttrWrap, bindablefield):
    signals = ['change']

    def __init__(self, caption=u'',
                 width_cap=conf.sizes['wgtFieldBoxDb1'][0], bindf=None, enterIsTab=False,readonly=False,cor=None):

        self._lastvalue = ''
        self._value = ''
        self.dirty = False
        self.caption = caption
        self._enterIsTab = enterIsTab
        self.capField = cap = urwid.Text(nisk.util.asUnicode((u'', caption)))
        # self.capField = urwid.Text([('key', caption[:1]), caption[1:]])
        self.textField = urwid.Edit('')
        self.textField.multiline = not enterIsTab
        urwid.connect_signal(self.textField, 'change', self.edit_changed)

        if not cor:
            cor = ('field', 'field_of')
        if len(cor) == 3:
            cap = urwid.AttrWrap(cap,cor[2])
        if len(cor) == 4:
            cap = urwid.AttrWrap(cap,cor[2],cor[3])
        
        self.readonly = readonly
        self.readonlyField = Text('')
        if readonly:
            field = urwid.AttrWrap(self.readonlyField,cor[0],cor[1])
        else:
            field = urwid.AttrWrap(self.textField,cor[0],cor[1])

        x = urwid.Columns([('fixed',  2, urwid.Text('* ')),('fixed',  width_cap,cap),
            field]
            , dividechars=0, focus_column=2)

        self.__super.__init__(x,cor[0])

    def setValue(self, txt, writelast=True):
        if self.readonly:
            s = str(txt) if txt else ''
            self.readonlyField.set_text(s)

        # nisk.util.dump([txt, type(txt)], self.caption)
        if isinstance(txt, unicode):
            try:
                txt = txt.encode('utf-8')
            except Exception, e:
                logging.exception(e)
                # nisk.util.dump(txt, self.caption)

        self._value = txt
        if writelast:
            self._lastvalue = txt

        if isinstance(self._value, basestring):
            pass
        elif self._value is None:
            self._value = ''
        else:
            self._value = ''

        try:
            self.textField.set_edit_text(self._value)
        except Exception, e:
            logging.exception(e)
            self.textField.set_edit_text('erro!')

    def changeValue(self, txt):
        self.setValue(txt, writelast=False)

    def edit_changed(self, x, d, *arg):
        if not nisk.util.isEquivalent(d, self._lastvalue):
            urwid.emit_signal(self, 'change', self, d)

    def keypress(self, size, key):
        key = self.__super.keypress(size, key)
        ##todo
        # urwid.AttrWrap(self.codField, 'dark red', 'yellow')
        #
        # self.codField._invalidate()
        if key == "tab":
            return 'down'

        if key == "enter" and self._enterIsTab:  # and not self.multiline:
            return 'down'

        elif key == "shift tab":
            return 'up'
        
        elif key == "f4":
            # nisk.util.wxtext.winx()
            ''''''
        elif key == "f5":
            # nisk.util.paralelo(nisk.util.wxtext.win)
            pass
            ''''''
        else:
            # key wasn't handled
            return key

    def edit_tk(self):    
        '''
        from Tkinter import *
        import ttk

        root = Tk()
        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        
        feet = StringVar()
        feet.set(self.GetValue())
        feet_entry = ttk.Entry(mainframe, width=37, textvariable=feet)
        feet_entry.grid(column=2, row=1, sticky=(W, E))

        for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

        feet_entry.focus()
        print 'going-on'
        root.mainloop()
        '''
        print   'out ok'

    def GetValue(self):
        x = self.textField.get_edit_text()
        # nisk.util.dump([x, type(x)], self.caption)

        x = x.decode('utf-8')

        self._value = x

        # nisk.util.dump([x, type(x)], self.caption)

        return self._value

    def _connect_signal(self, name, callback):
        return urwid.connect_signal(self, name, callback)


######################################################################
class wgtIntFieldBox(AttrWrap, bindablefield):
    signals = ['change']

    def __init__(self, caption=u'',
                 width_cap=conf.sizes['wgtFieldBoxDb1'][0], bindf=None, enterIsTab=False,cor=None,readonly=False):

        self._TextValue = ''
        self.dirty = False
        self._enterIsTab = enterIsTab
        self.capField = urwid.Text(nisk.util.asUnicode((u'', caption)))
        self.textField = wgtIntEdit('')
        urwid.connect_signal(self.textField, 'valuechange', self.edit_changed)
        self.readonlyField = Text('')
        
        if not cor:
            cor = ('field', 'field_of')
        self.readonly = readonly
        if readonly:
            field = urwid.AttrWrap(self.readonlyField,cor[0],cor[1])
        else:
            field = urwid.AttrWrap(self.textField,cor[0],cor[1])

        x = Columns([('fixed',  2, urwid.Text('* ')),
                     ('fixed',  width_cap,self.capField),
            urwid.AttrWrap(field,cor[0],cor[1])]            , dividechars=0, focus_column=2)

        self.__super.__init__(x,cor[0])

    def setValue(self, txt):
        if self.readonly:
            s = str(txt) if txt else ''
            self.readonlyField.set_text(s)
        return self.textField.setvalue(txt)

    def edit_changed(self, x, d, *arg):
        if self.textField._checamudou():
            urwid.emit_signal(self, 'change', self, d)

    def keypress(self, size, key):
        key = self.__super.keypress(size, key)
        ##todo
        # urwid.AttrWrap(self.codField, 'dark red', 'yellow')
        #
        # self.codField._invalidate()
        if key == "tab":
            return 'down'

        if key == "enter" and self._enterIsTab:  # and not self.multiline:
            return 'down'

        elif key == "shift tab":
            return 'up'

        elif key == "f4":
            # nisk.util.paralelo(self.seleciona_popup)
            pass

        else:
            # key wasn't handled
            return key

    def GetValue(self):
        return self.textField.value()

    def _connect_signal(self, name, callback):
        return urwid.connect_signal(self, name, callback)


######################################################################
class wgtDateFieldBox(AttrWrap, bindablefield):
    signals = ['change']

    def __init__(self,_widgetpai, caption=u'',
                 width_cap=conf.sizes['wgtFieldBoxDb1'][0], bindf=None, enterIsTab=False, dformat='%d/%m/%Y %H:%M',cor=None,readonly=False):
        self._widgetpai = _widgetpai
        self._TextValue = ''
        self.dirty = False
        self._enterIsTab = enterIsTab
        self.capField = urwid.Text(nisk.util.asUnicode((u'', caption)))
        self.textField = wgtDateEdit()
        self.dformat = dformat
        urwid.connect_signal(self.textField, 'valuechange', self.edit_changed)
        urwid.connect_signal(self.textField, 'focusIn', self._OnFocusIn)
        urwid.connect_signal(self.textField, 'focusOut', self._OnFocusOut)
        
        self.readonly = readonly
        if not cor:
            cor = ('field', 'field_of')

        self.readonlyField = Text('')
        if readonly:
            field = urwid.AttrWrap(self.readonlyField,cor[0],cor[1])
        else:
            field = urwid.AttrWrap(self.textField,cor[0],cor[1])
        
        x = Columns([('fixed',  2, urwid.Text('* ')),
                     ('fixed',  width_cap,self.capField),
            urwid.AttrWrap(field,cor[0],cor[1])]            , dividechars=0, focus_column=2)

        self.__super.__init__(x,cor[0])

    def setValue(self, v):
        # r = self.lck.acquire()
        self.setvalue(v)
        # if r:
        # self.lck.release()

    def _OnFocusIn(self, x=None, y=None):
        self._widgetprocessa('dlg_statusbar_put', "Insira a data no formato DD/MM/AA", self)
        pass

    def _OnFocusOut(self, x=None, y=None):
        self._widgetprocessa('dlg_statusbar_pop', None, self)
        pass

    def edit_changed(self, x, d, *arg):
        # r = self.lck.acquire(False)
        # if r:
        if self.textField._checamudou():
            urwid.emit_signal(self, 'change', self, d)
            nisk.util.dump((self.textField.value(), self.textField._lastlastvalue, self.textField._checamudou()),
                           'change date')

    def keypress(self, size, key):
        key = self.__super.keypress(size, key)
        if key == "tab":
            return 'tab'

        if key == "enter" and self._enterIsTab:
            return 'tab'

        elif key == "shift tab":
            return 'up'

        else:
            return key

    def GetValue(self):
        return self.textField.value()

    def _connect_signal(self, name, callback):
        return urwid.connect_signal(self, name, callback)

    def setvalue(self, v):
        if self.readonly:
            s = str(v) if txt else ''
            self.readonlyField.set_text(s)
        return self.textField.setvalue(v)


class wgtFieldBoxDb_display(urwid.Text):
    ''' TENTATIVA DE RESOLVER BUG DE RENDERIZAÇÃO'''
    def __init__(self,*arg,**kw):
        self._size = None
        super(self.__class__, self).__init__(*arg,**kw)

    def render(self, size, focus=False):
        self._size = size
        return super(self.__class__, self).render(size,focus)

    def set_text(self,markup):
        if self._size:
            if len(markup)> self._size[0]:
                markup = markup[0:self._size[0]]
        return super(self.__class__, self).set_text(            markup)

######################################################################
class wgtFieldBoxDb(AttrWrap, bindablefield):
    signals = ['change']
    defaultPopupSelector = None
    defaultConsultor = None

    def __init__(self, ltabela='', tabela='', caption=u'',
                 consultor=None,
                 width_cap=conf.sizes['wgtFieldBoxDb1'][0],
                 width_cod=conf.sizes['wgtFieldBoxDb1'][1], bindf=None, params=None,cor=None,readonly=False):

        self.params = params if params else {}

        if consultor is None:
            if wgtFieldBoxDb.defaultConsultor is None:
                self.consultor = None
            else:
                self.consultor = wgtFieldBoxDb.defaultConsultor
        else:
            self.consultor = consultor

        sttbt = [('title', "Selecionar"), ('key', "F4")]
        if nisk.util.defaultv(self.params, 'canedit', True):
            sttbt.append([" | ", ('title', "Editar"), ('key', "F5")])
        self.params['statusbartext'] = sttbt

        self.popupselector = None
        self._CodValue = None
        self.ltabela = ltabela
        self.tabela = tabela
        self._TextValue = ''
        self.dirty = False
        self._orm = None
        self._iniciado = False

        self.capField = cap = urwid.Text(nisk.util.asUnicode((u'', caption)))

        self.codField = wgtIntEdit()
        self.lastCod = nisk.util.asInt(self.codField.value())

        self.textField =  wgtFieldBoxDb_display('')
        urwid.connect_signal(self.codField, 'valuechange', self.edit_changed)
        urwid.connect_signal(self.codField, 'focusIn', self._OnFocusIn)
        urwid.connect_signal(self.codField, 'focusOut', self._OnFocusOut)

        
        self.readonly = readonly
        if not cor:
            cor = ('field', 'field_of')

        self.readonlyField = urwid.Text('')
        if readonly:
            field = urwid.AttrWrap(self.readonlyField,cor[0],cor[1])
        else:
            field = urwid.AttrWrap(self.codField,cor[0],cor[1])

        if len(cor) == 3:
            cap = urwid.AttrWrap(cap,cor[2])
        if len(cor) == 4:
            cap = urwid.AttrWrap(cap,cor[2],cor[3])

        self._col = urwid.Columns([('fixed',  2, urwid.Text('* ')),('fixed', width_cap, cap),
            ('fixed', width_cod, urwid.AttrWrap(field, cor[0],cor[1])),
            ('fixed', 1, urwid.Text('-')),
            urwid.AttrWrap(self.textField, cor[0],cor[1])], dividechars=0, focus_column=2)
        
        self.__super.__init__(self._col,cor[0])

    def _OnFocusIn(self, x=None, y=None):
        if nisk.util.defaultv(self.params, 'showstatusbartext', True):
            self._widgetprocessa('dlg_statusbar_put', nisk.util.defaultv(self.params, 'statusbartext', ''), self)
        pass

    def _OnFocusOut(self, x=None, y=None):
        if nisk.util.defaultv(self.params, 'showstatusbartext', True):
            self._widgetprocessa('dlg_statusbar_pop', None, self)
        pass

    def edit_changed(self, x, d, *arg):
        if self.codField.value() != self.codField._lastlastvalue:
            self.load(self.codField.value())
            # urwid.emit_signal(self, 'change', self, d)
        # nisk.util.dump((self.codField.value(), self.codField._lastlastvalue),
        # 'change')
        pass

    def setValue(self, cod, force=False):
        try:
            self.load(cod, force)
        except:
            pass

    def load(self, cod, force=False):
        c, t, r, o = self.consulta(cod)
        self.codField.setvalue(c)
        self.readonlyField.set_text(nisk.util.asstr(c))
        self._orm = o
        if r:
            self.textField.set_text(t)
            self.readonlyField.set_text(t)
            if self.lastCod != c:
                self.lastCod = c
                # logging.debug('l1')
                if self._iniciado:
                    urwid.emit_signal(self, 'change', self, self.GetValue())
        elif force:
            self.codField.setvalue(None)
            self.readonlyField.set_text(nisk.util.asstr(None))
            self.textField.set_text('')
            self.readonlyField.set_text('')
            self.lastCod = None
            if 1:  # self._iniciado:
                urwid.emit_signal(self, 'change', self, self.GetValue())
        self._iniciado = True
        # urwid.CanvasCache._widgets.clear()

    def consulta(self, cod):
        err = 1
        d = dt = None
        nome = ''
        # nisk.util.dump(cod, 'consulta sql cod')
        if not self.consultor is None:
            if cod > 0:
                d = self.consultor(nisk.util.asInt(cod), tab=self.tabela, ltab=self.ltabela)
                if not d is None:
                    dt = d[0]
                    nome = d[1]
            if not dt is None:
                return cod, nome, True, d
                err = 0
        if err:
            return self.lastCod, None, False, self._orm

    def keypress(self, size, key):
        key = super(wgtFieldBoxDb, self).keypress(size, key)
        ##todo
        # urwid.AttrWrap(self.codField, 'dark red', 'yellow')
        #
        # self.codField._invalidate()
        if key == "tab" or key == "enter":
            # self.load(self.codField.value())
            return 'down'

        elif key == "shift tab":
            # self.load(self.codField.value())
            return 'up'

        elif key == "f4":
            x = self.popupselector
            if x is None:
                if not wgtFieldBoxDb.defaultPopupSelector is None:
                    x = wgtFieldBoxDb.defaultPopupSelector
            if x:
                # nisk.util.paralelo(x, [self])
                x(self)

        elif key == "f2":
            tk.window()

        elif key == "f5":
            self._widgetprocessa('dlg_statusbar_put',
                                 [('title', "Selecionar"), ('key', "F4"), " | ", ('title', "Editar"), ('key', "F5")],
                                 self)

        else:
            # key wasn't handled
            return key

    def GetValue(self):
        # return self._orm
        return self.codField._lastvalue

    def _connect_signal(self, name, callback):
        return urwid.connect_signal(self, name, callback)


######################################################################
class wgtComboBox(Edit):
    signals = ['onselect']

    def Clear(self):
        pass

    def AppendItems(self, items):
        pass

    def SetValue(self, val):
        self.set_edit_text(val)

    def GetValue(self):
        return self.get_text()

    def SetStringSelection(self, strr):
        pass

    def Clear(self):
        pass

    def SetSelection(self, index):
        pass

    def _connect_signal(self, name, callback):
        return urwid.connect_signal(self, name, callback)


######################################################################
class wgtListBox(urwid.ListBox):
    signals = ['onselect']

    def _connect_signal(self, name, callback):
        return urwid.connect_signal(self, name, callback)

    def AppendItems(self, lst):
        pass


######################################################################
class DataGrid(Edit):
    def ClearGrid(self, *args):
        pass

    def SetCellValue(self, *args):
        pass

    def SelectRow(self, *args):
        pass

    def AutoSize(self, *args):
        pass

    def GetValue(self):
        return self.get_text()

    def _connect_signal(self, name, callback):
        return urwid.connect_signal(self, name, callback)


######################################################################
class wgtButton(urwid.Button):
    def Disable(self):
        pass

    def Enable(self):
        pass

    def _connect_signal(self, name, callback):
        return urwid.connect_signal(self, name, callback)


######################################################################
def hamilton_allocation(counts, alloc):
    """
    Implements the Hamilton Method (Largest remainder method) to calculate
    integral ratios. (Like it is used in some elections.)

    counts -- list of integers ('votes per party')
    alloc -- total amount to be allocated ('total amount of seats')
    """

    total_counts = sum(counts)
    quotas = [float(count) * alloc / total_counts for count in counts]

    fracts = []
    for (i, fp) in enumerate(quotas):
        fracts.append((math.modf(fp)[0], i))

    fracts.sort()
    fracts.reverse()

    results = [int(math.modf(quota)[1]) for quota in quotas]
    remainder = alloc - sum(results)

    for i in range(remainder):
        results[fracts[i][1]] += 1

    return results


######################################################################
class HScrollBar(urwid.BoxWidget):
    """
    A scrollbar.
    """

    def __init__(self, handle, background, middle, top, bottom):
        """
        handle -- (character, attribute) for the drawing of the scrollbar's
                  handle
        background -- (character, attribute) for the drawing of the background
        middle -- number of visible rows of the corresponding widget
        top -- number of lines above visible rows of the corresponding widget
        bottom -- number of lines below visible rows of the corresponding
                  widget
        """

        self.handle_widget = urwid.SolidFill(handle[0])
        if handle[1] is not None:
            self.background_widget = urwid.AttrWrap(self.handle_widget,
                                                    handle[1])

        self.background_widget = urwid.SolidFill(background[0])
        if background[1] is not None:
            self.background_widget = urwid.AttrWrap(self.background_widget,
                                                    background[1])
        self.middle = middle
        self.top = top
        self.bottom = bottom

        self.handle_grab_pos = -1
        self.handle_moved = 0

    def selectable(self):
        "Not selectable."""
        return False

    def mouse_event(self, (maxcol, maxrow), event, button, col, row, focus):
        """
        Handle mouse events.
        """

        (middle, top, bottom) = hamilton_allocation([self.middle, self.top,
                                                     self.bottom], maxcol)

        if (event == "mouse press" and button == 1 and row >= top and row < middle + top):

            # User grabs handle with left mouse button
            self.handle_grab_pos = row
            return True

        elif self.handle_grab_pos >= 0 and event == "mouse release":
            # User releases handle
            self.handle_moved += row - self.handle_grab_pos
            self.handle_grab_pos = -1
            return True

        else:
            return False

    def render(self, (maxcol, maxrow), focus=False):
        """
        Render the ScrollBar as a canvas and return it.
        """

        (middle, top, bottom) = hamilton_allocation([self.middle, self.top,
                                                     self.bottom], maxcol)

        # nisk.util.dump((maxcol, maxrow))
        # nisk.util.dump((middle, top, bottom))
        pile = urwid.Columns([(top, self.background_widget),
                              (bottom, self.background_widget),
                              (middle, self.handle_widget)])

        return pile.render((maxcol, maxrow), focus)

    def read_move(self, maxrow, length):
        """
        Updates the position of the scrollbar and returns the amount of lines
        the corresponding widget has to be scrolled.

        maxrow -- number of displayed rows of the widget to which the
                  scrollbar belongs
        length -- overall length of the widgets list of that widget

        """

        moved = int(float(self.handle_moved) / self.middle * length)
        self.handle_moved = 0

        # Ensure that we stay in a correct range:
        if self.top + moved < 0:
            moved -= self.top + moved

        if self.bottom - moved < 0:
            moved += self.bottom - moved

        self.top += moved
        self.bottom -= moved

        return moved


######################################################################
class ScrollBar(urwid.BoxWidget):
    """
    A scrollbar.
    """

    def __init__(self, handle, background, middle, top, bottom):
        """
        handle -- (character, attribute) for the drawing of the scrollbar's
                  handle
        background -- (character, attribute) for the drawing of the background
        middle -- number of visible rows of the corresponding widget
        top -- number of lines above visible rows of the corresponding widget
        bottom -- number of lines below visible rows of the corresponding
                  widget
        """

        self.handle_widget = urwid.SolidFill(handle[0])
        if handle[1] is not None:
            self.background_widget = urwid.AttrWrap(self.handle_widget,
                                                    handle[1])

        self.background_widget = urwid.SolidFill(background[0])
        if background[1] is not None:
            self.background_widget = urwid.AttrWrap(self.background_widget,
                                                    background[1])

        self.middle = middle
        self.top = top
        self.bottom = bottom

        self.handle_grab_pos = -1
        self.handle_moved = 0

    def selectable(self):
        "Not selectable."""
        return False

    def mouse_event(self, (maxcol, maxrow), event, button, col, row, focus):
        """
        Handle mouse events.
        """

        (middle, top, bottom) = hamilton_allocation([self.middle, self.top,
                                                     self.bottom], maxrow)

        if (event == "mouse press" and button == 1 and row >= top and row < middle + top):

            # User grabs handle with left mouse button
            self.handle_grab_pos = row
            return True

        elif self.handle_grab_pos >= 0 and event == "mouse release":
            # User releases handle
            self.handle_moved += row - self.handle_grab_pos
            self.handle_grab_pos = -1
            return True

        else:
            return False

    def render(self, (maxcol, maxrow), focus=False):
        """
        Render the ScrollBar as a canvas and return it.
        """

        (middle, top, bottom) = hamilton_allocation([self.middle, self.top,
                                                     self.bottom], maxrow)

        pile = urwid.Pile([('fixed', top, self.background_widget),
                           ('fixed', middle, self.handle_widget),
                           ('fixed', bottom, self.background_widget)])

        return pile.render((maxcol, maxrow), focus)

    def read_move(self, maxrow, length):
        """
        Updates the position of the scrollbar and returns the amount of lines
        the corresponding widget has to be scrolled.

        maxrow -- number of displayed rows of the widget to which the
                  scrollbar belongs
        length -- overall length of the widgets list of that widget

        """

        moved = int(float(self.handle_moved) / self.middle * length)
        self.handle_moved = 0

        # Ensure that we stay in a correct range:
        if self.top + moved < 0:
            moved -= self.top + moved

        if self.bottom - moved < 0:
            moved += self.bottom - moved

        self.top += moved
        self.bottom -= moved

        return moved


######################################################################
class SBListBox(urwid.WidgetWrap):
    """
    A ListBox with a scroll bar.
    """

    def __init__(self, body, handle=(u"#", "handle"), background=(u"|", "scrollbar_bg")):
        """
        body -- list or a SimpleListWalker object that contains the
                widgets to be displayed inside the list box.
                The __len__ attribute must be implemented!
        handle -- (character, attribute) for the drawing of the scrollbar's
                  handle
        background -- (character, attribute) for the drawing of the scrollbar's
                      background
        """

        if isinstance(body, urwid.ListBox):
            self.length = len(body.body)
            self.listbox = body
        elif isinstance(body, list):
            self.length = len(body)
            self.listbox = urwid.ListBox(body)
        elif isinstance(body, urwidtrees.TreeBox):
            self.length = len(body._outer_list.body._tree._treelist)
            self.listbox = body._outer_list
        else:
            raise Exception

        self.scrollbar = ScrollBar(handle, background, 1, 0, 0)
        pscroll = Pile([('pack', Text(u'\u25b2')), ('weight', 1, self.scrollbar), ('pack', Text(u"\u25bc"))])
        # self.scrollbar = HScrollBar(handle, background, 1, 1, 1);
        self.columns = urwid.Columns([# ("fixed", 1, pscroll),
            ("weight", 1, self.listbox),
            ("fixed", 1, pscroll)],
            dividechars=1)

        # self.pile = urwid.Pile([
        # ('weight', 1, self.columns),
        # ( 1, self.scrollbar)]
        # );

        urwid.WidgetWrap.__init__(self, self.columns)

    def calc_sb_midtopbot(self, size):
        """
        Calculate middle, top, bottom for the scrollbar.
        """

        (middle, top, bottom) = self.listbox.calculate_visible(size)
        self.scrollbar.middle = min(size[1], self.length)
        middle2 = middle[2]
        if type(middle2) is tuple:
           middle2 = 0# middle2[0]
        self.scrollbar.top = middle2 - len(top[1])
        self.scrollbar.bottom = self.length - middle2 - len(bottom[1]) - 1
        self.scrollbar._invalidate()

    def render(self, size, focus=False):
        """
        Render the SBListBox as a canvas and return it.
        """

        self.calc_sb_midtopbot(size)
        return self.columns.render(size, focus)

    def mouse_event(self, size, event, button, col, row, focus):
        """
        Handle mouse events.
        """

        if event == "mouse release" and self.scrollbar.handle_grab_pos >= 0:
            # If the handle is grabbed, pretend that every release is over the
            # scrollbar:
            col = size[0] - 1

        handled = self.columns.mouse_event(size, event, button, col, row,
                                           focus)

        # Scroll the listbox according to handle movement:
        moved = self.scrollbar.read_move(size[1], self.length)

        position = self.listbox.get_focus()[1]
        (offset, inset) = self.listbox.get_focus_offset_inset(size)

        assert (position + moved >= 0) or (position + moved <= self.length), \
            "Move out of list range: %i\n" % (position + moved)

        self.listbox.change_focus(size, position + moved, offset)

        return handled


######################################################################
class LineBox(WidgetDecoration, WidgetWrap):
    id = None

    def __init__(self, original_widget, title="",
                 tlcorner=u'\u250c', tline=u'\u2500',
                 lline=u'\u2502', trcorner=u'\u2510',
                 blcorner=u'\u2514', rline=u'\u2502',
                 bline=u'\u2500', brcorner=u'\u2518',
                 id=None):

        self.id = id

        tline, bline = Divider(tline), Divider(bline)
        lline, rline = SolidFill(lline), SolidFill(rline)
        tlcorner, trcorner = Text(tlcorner), Text(trcorner)
        blcorner, brcorner = Text(blcorner), Text(brcorner)

        self.title_widget = Text(self.format_title(title))
        self.tline_widget = Columns([tline,
            ('flow', self.title_widget),
            tline,])

        top = Columns([('fixed', 1, tlcorner),
            self.tline_widget,
            ('fixed', 1, trcorner)])

        middle = Columns([('fixed', 1, lline),
            original_widget,
            ('fixed', 1, rline),], box_columns=[0, 2], focus_column=1)

        bottom = Columns([('fixed', 1, blcorner), bline, ('fixed', 1, brcorner)])

        pile = Pile([('flow', top), middle, ('flow', bottom)], focus_item=1)

        WidgetDecoration.__init__(self, original_widget)
        WidgetWrap.__init__(self, pile)

    def format_title(self, text):
        text = str(text)
        if isinstance(text, basestring):
            if len(text) > 0:
                text = " %s " % text
                return text
            else:
                text = ''
                return text
        else:
            text = "? %s ?" % text
            return text

    def GetId(self):
        return self.id

    def set_title(self, text):
        self.title_widget.set_text(self.format_title(text))
        self.tline_widget._invalidate()

    def Bind(self, event, handler, source=None):
        urwid.connect_signal(self, event, handler, id)


######################################################################
class FrameBox(urwid.Frame):
    id = None

    def __init__(self, original_widget,
                 id=None):
        self.id = id

        urwid.Frame.__init__(self, original_widget)

    def GetId(self):
        return self.id

    def Bind(self, event, handler, source=None):
        urwid.urwid.connect_signal(self, event, handler, id)


######################################################################
class HMenu(urwid.Columns):
    class MenuButton(urwid.Button):
        def __init__(self, caption, callback, shortcutchar='&', showshort=True, norepeatlist=None):
            super(HMenu.MenuButton, self).__init__("")
            urwid.connect_signal(self, 'click', callback)
            self.shortkey = None
            bulet = True

            x = caption if isinstance(caption, basestring) else (caption[0] if isinstance(caption, list) and len(caption) > 0 else None)

            if isinstance(x, basestring):
                # nisk.util.dump(('a',x))
                x = x.split(shortcutchar, 1)
                # nisk.util.dump(('b',x))
                if len(x) == 2 and len(x[1]) > 0:
                    # nisk.util.dump(('c',x))
                    y = x[1][0]
                    x[1] = x[1][1:]
                    yx = y

                    if not norepeatlist is None and not y is None:
                        # nisk.util.dump((norepeatlist, y, caption))
                        if y not in norepeatlist:
                            norepeatlist.append(y)
                            self.shortkey = y.lower()
                            yx = ('InfoFooterHotkey', y.upper()) if showshort else yx
                            # nisk.util.dump((norepeatlist, y))
                    # nisk.util.dump(('d',x))
                    if isinstance(caption, basestring):
                        caption = [u'  * ', x[0], yx, x[1]]
                        bulet = False
                    elif isinstance(caption, list) and len(caption) > 0:
                        del caption[0]
                        caption.insert(0, x[1])
                        caption.insert(0, yx)
                        caption.insert(0, x[0])
                        caption.insert(0, u'  * ')
                        bulet = False
            if bulet:
                caption = [u'  * ', caption]
            # logging.debug(str(caption))
            #
            # self._w = urwid.AttrMap(urwid.Text(
            # caption), 'options', 'selected')
            self._w = urwid.AttrMap(urwid.SelectableIcon(caption, 2), 'options', 'selected')

    class SubMenu(urwid.WidgetWrap):
        def __init__(self, caption, choices, parent=None, norepeatlist=None):
            menubutton = HMenu.MenuButton([caption, u" "],
                self.open_menu, norepeatlist=norepeatlist)
            super(HMenu.SubMenu, self).__init__(menubutton)
            self.shortcut = menubutton.shortkey
            self.parent = parent
            line = urwid.Divider(u'-')
            self.choices = choices
            listbox = urwid.ListBox(urwid.SimpleFocusListWalker([urwid.AttrMap(HMenu.MenuButton([caption, u" "],
                                                                        self.menu_back, showshort=False),
                                                                        'heading'),
                                                                    urwid.AttrMap(line, 'line'),
                                                                    urwid.Divider()] + choices + [urwid.Divider()]))
            self.menu = urwid.AttrMap(listbox, 'options_nf','options')

        def open_menu(self, button):
            self.parent.open_box(self.menu, self)

        def menu_back(self, button, *args):
            self.parent.back()

        def check_short(self, key):
            if isinstance(key, basestring):
                for x in self.choices:
                    # nisk.util.dump([key, x.shortcut])
                    if not x is None and not x.shortcut is None and x.shortcut.lower() == key.lower():
                        x.open_menu(x)
                        return True
            return False

    class Choice(urwid.WidgetWrap):
        def __init__(self, caption, cb=None, dados=None, parent=None, norepeatlist=None):
            h = HMenu.MenuButton([caption, u" "],
                self.item_chosen, norepeatlist=norepeatlist)

            self.shortcut = h.shortkey
            self.cb = cb
            self.dados = dados
            super(HMenu.Choice, self).__init__(h)
            self.parent = parent
            self.caption = caption
            # line = urwid.Divider(u'-')

            # listbox = urwid.ListBox(urwid.SimpleFocusListWalker([
            # urwid.AttrMap(HMenu.MenuButton(
            # [caption, u"*"],
            # self.menu_back),
            # 'heading'),
            # urwid.AttrMap(line, 'line'),
            # urwid.Divider()] + [urwid.Divider()]))
            # self.menu = urwid.AttrMap(listbox, 'options')

        def menu_back(self, button):
            self.parent.back()

        def open_menu(self, button):
            self.item_chosen(button)

        def item_chosen(self, button):
            if not self.cb is None:
                self.cb(self.dados)
                self.parent.first()

    def keypress(self, size, key):
        key = self.__super.keypress(size, key)

        if key in ('esc', 'ESC'):
            if self.top.back():
                return None
        if key in ('f1', 'F1'):
            self.invert()
            return None

        x = self.checkLocalKey(key)
        return x

    def checkLocalKey(self, key):
        if not key is None and len(key) == 1:
            if not self.top.menu is None:
                if self.top.menu.check_short(key):
                    return None
        return key

    def opt(key):
        pass

    def setwid(self, wid):
        self.wid = wid

        if len(self.contents) == 1:
            del self.contents[0]
        else:
            del self.contents[1]

        self.contents.insert(0, (self.wid, self.options('weight', 1)))
        self.onmenuopen()

    def onmenuclose(self):
        if len(self.contents) == 2:
            pass
            # del self.contents[0]

    def onmenuopen(self):
        if not self.opts is None:
            if len(self.contents) == 1:
                self.contents.insert(0, (urwid.AttrMap(self.top, 'options_nf','options',), self.options('given', self.wdt)))
                self.top.open_box(self.opts.menu, self.opts)
        self.set_focus_column(0)

    def invert(self):
        if len(self.contents) == 2:
            self.onmenuclose()
        elif len(self.contents) == 1:
            self.onmenuopen()

    class HorizontalBoxes(urwid.Frame):
        def __init__(self, onclose=None):
            self.pilha = nisk.util.pilha()
            self.onclose = onclose
            self.menu = None
            super(HMenu.HorizontalBoxes, self).__init__(urwid.Filler(urwid.Divider()))

        def back(self):
            # logging.debug('hmenub' + str(len(self.pilha.dados)))
            o = len(self.pilha.dados) > 0 if not self.onclose is None else len(self.pilha.dados) > 1
            if o:
                x = self.pilha.desempilha()
                if not x is None:
                    (self.body, self.menu) = x
                    if self.pilha.vazia() and not self.onclose is None:
                        self.onclose()
                    return True
            return False

        def first(self):
            o = len(self.pilha.dados) > 0 if not self.onclose is None else len(self.pilha.dados) > 1
            y = 2  # if len(self.pilha.dados) > 1 else 1
            if o:
                del self.pilha.dados[y:]
                x = self.pilha.topo()
                if x:
                    (self.body, self.menu) = x
                    if (self.pilha.vazia() or not self.menu) and self.onclose:
                        self.onclose()
                    return True
            return False

        def open_box(self, box, menu):
            # logging.debug('hmenuo' + str(len(self.pilha.dados)))
            self.pilha.empilha((self.body, self.menu))
            self.body = box
            self.menu = menu

    def __init__(self, opts, wid, defaultcb=None, width=24, selfclose=False):
        x = self.onmenuclose if selfclose else None
        self.top = HMenu.HorizontalBoxes(onclose=x)
        self.wdt = width
        self.wid = wid
        self.defaultcb = defaultcb

        def resolve(trecho, nicho, norepeatlist=None):
            if isinstance(trecho, basestring):
                nicho.append(HMenu.Choice(trecho, cb=defaultcb, parent=self.top, norepeatlist=norepeatlist))
            elif isinstance(trecho, tuple):
                if len(trecho) == 2 and isinstance(trecho[1], list):
                    o = []
                    l = []
                    for x in trecho[1]:
                        resolve(x, o, norepeatlist=l)
                    nicho.append(HMenu.SubMenu(trecho[0], o, parent=self.top, norepeatlist=norepeatlist))
                elif len(trecho) > 1 and hasattr(trecho[1], '__call__'):
                    d = trecho[2] if len(trecho) > 2 else None
                    nicho.append(HMenu.Choice(trecho[0], cb=trecho[1], dados=d, parent=self.top, norepeatlist=norepeatlist))
                elif len(trecho) > 0:
                    d = trecho[1] if len(trecho) > 1 else None
                    nicho.append(HMenu.Choice(trecho[0], cb=defaultcb, dados=d, parent=self.top, norepeatlist=norepeatlist))

        o = []
        l = []
        resolve(opts, o, norepeatlist=l)
        if len(o) > 0:
            self.opts = o[0]

        if wid is None:
            wid = urwid.Filler(urwid.Divider())

        urwid.Columns.__init__(self, [("weight", 1, wid)],
                               dividechars=1)
