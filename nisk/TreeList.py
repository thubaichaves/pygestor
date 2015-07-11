import urwid, logging
from urwid.signals import connect_signal

import nisk.TUI


class FlagFileWidget(urwid.TreeWidget):
    # apply an attribute to the expand/unexpand icons
    unexpanded_icon = urwid.AttrMap(urwid.TreeWidget.unexpanded_icon,
                                    'dirmark')
    expanded_icon = urwid.AttrMap(urwid.TreeWidget.expanded_icon,
                                  'dirmark')

    def __init__(self, node):
        self.__super.__init__(node)
        # insert an extra AttrWrap for our own use
        self._w = urwid.AttrWrap(self._w, None)
        self.flagged = False
        self.update_w()

    def selectable(self):
        return True

    def keypress(self, size, key):
        """allow subclasses to intercept keystrokes"""
        key = self.__super.keypress(size, key)
        if key:
            key = self.unhandled_keys(size, key)
        return key

    def unhandled_keys(self, size, key):
        """
        Override this method to intercept keystrokes in subclasses.
        Default behavior: Toggle flagged on space, ignore other keys.
        """
        return key
        if key == " ":
            self.flagged = not self.flagged
            self.update_w()
        else:
            return key

    def update_w(self):
        """Update the attributes of self.widget based on self.flagged.
        """
        if self.flagged:
            self._w.attr = 'flagged'
            self._w.focus_attr = 'flagged focus'
        else:
            self._w.attr = 'body'
            self._w.focus_attr = 'focus'


class FileTreeWidget(FlagFileWidget):
    def __init__(self, node):
        self.__super.__init__(node)
        key = node.get_key()
        add_widget(key, self)

    def get_display_text(self):
        return self.get_node().get_value()


class EmptyWidget(urwid.TreeWidget):
    """A marker for expanded directories with no contents."""

    def get_display_text(self):
        return ('flag', '(empty directory)')


class ErrorWidget(urwid.TreeWidget):
    """A marker for errors reading directories."""

    def get_display_text(self):
        return ('error', "(error/permission denied)")


class DirectoryWidget(FlagFileWidget):
    def __init__(self, node):
        self.__super.__init__(node)
        key = node.get_key()
        add_widget(key, self)

    def get_display_text(self):
        node = self.get_node()
        return node.get_value()


class FileNode(urwid.TreeNode):
    def __init__(self, _key, parent=None, dados={}):
        self.dados = dados
        self.key = _key
        dado = dados[self.key]
        level = dado['level'] + 1
        nome = dado['nome']
        self.pai = dado['pai']

        urwid.TreeNode.__init__(self, nome, key=self.key, parent=parent,
                                depth=level)

    def load_parent(self):
        # if(not self.pai == self.key):
        parent = DirectoryNode(self.pai, dados=self.dados)
        parent.set_child_node(self.get_key(), self)
        return parent
        # return None

    def load_widget(self):
        return FileTreeWidget(self)


class EmptyNode(urwid.TreeNode):
    def load_widget(self):
        return EmptyWidget(self)


class ErrorNode(urwid.TreeNode):
    def load_widget(self):
        return ErrorWidget(self)


class DirectoryNode(urwid.ParentNode):
    def __init__(self, _key, parent=None, dados={}):
        self.dados = dados
        self.key = _key
        dado = dados[self.key]
        self.level = dado['level'] + 1
        self.dbid = dado['dbid']
        nome = dado['nome']
        self.pai = dado['pai']

        urwid.ParentNode.__init__(self, nome, key=self.key, parent=parent,
                                  depth=self.level)

    def load_parent(self):
        # if(not self.pai == self.key):
        parent = DirectoryNode(self.pai, dados=self.dados)
        parent.set_child_node(self.get_key(), self)
        return parent
        # return None

    def load_child_keys(self):
        keys = []
        nomes = []
        for n in self.dados.values():
            if n['pai'] == self.key and not n['pai'] == n['tid']:
                nomes.append([n['nome'], n['tid']])
        nomes.sort()
        for n in nomes:
            keys.append(n[1])
        return keys

    def load_child_node(self, key):
        if (key is None):
            return EmptyNode(None)
        else:
            for n in self.dados.values():
                if n['pai'] == key and not n['pai'] == n['tid']:
                    return DirectoryNode(key, parent=self, dados=self.dados)
            return FileNode(key, parent=self, dados=self.dados)

    def load_widget(self):
        return DirectoryWidget(self)


class FirstNode(urwid.ParentNode):
    def __init__(self, nome='', parent=None, dados={}):
        self.dados = dados

        urwid.ParentNode.__init__(self, nome, key=None, parent=parent,
                                  depth=0)

    def load_child_keys(self):
        keys = []
        nomes = []
        for n in self.dados.values():
            if n['pai'] == n['tid']:
                nomes.append([n['nome'], n['tid']])
        nomes.sort()
        for n in nomes:
            keys.append(n[1])
        return keys

    def load_child_node(self, key):
        if (key is None):
            return EmptyNode(None)
        else:
            for n in self.dados.values():
                if n['pai'] == key and not n['pai'] == n['tid']:
                    return DirectoryNode(key, parent=self, dados=self.dados)
            return FileNode(key, parent=self, dados=self.dados)

    def load_widget(self):
        return DirectoryWidget(self)


class TreeListBrowserBase:
    # palette = [
    # ('body', 'black', 'light gray'),
    # ('flagged', 'black', 'dark green', ('bold','underline')),
    # ('focus', 'light gray', 'dark blue', 'standout'),
    # ('flagged focus', 'yellow', 'dark cyan',
    # ('bold','standout','underline')),
    # ('head', 'yellow', 'black', 'standout'),
    # ('foot', 'light gray', 'black'),
    #    ('key', 'light cyan', 'black','underline'),
    #    ('title', 'white', 'black', 'bold'),
    #    ('dirmark', 'black', 'dark cyan', 'bold'),
    #    ('flag', 'dark gray', 'light gray'),
    #    ('error', 'dark red', 'light gray'),
    #    ]

    footer_text = [
        ('title', "Novo"), ('key', "F2"), ",",
        ('key', "UP"), ",", ('key', "DOWN"), ",",
        ('key', "PAGE UP"), ",", ('key', "PAGE DOWN"),
        "  "
    ]

    def __init__(self, tab=None, ltab=None, loader=None, tree=False):
        self.header = urwid.Edit()

        if loader is None:
            loader = self.FoolLoader

        self.loader = loader
        self.tree = tree
        self.tab = tab
        self.ltab = ltab
        self.search = ''

        connect_signal(self.header, "change", self.update)

        self.fn = FirstNode(nome='')
        self.tw = urwid.TreeWalker(self.fn)
        self.listbox = urwid.TreeListBox(self.tw)

        self.listbox.offset_rows = 3

        self.footer = urwid.AttrWrap(urwid.Text(self.footer_text),
                                     'foot')

        self.view = urwid.Frame(
            urwid.AttrWrap(self.listbox, 'body'),
            header=urwid.AttrWrap(self.header, 'head'),
            footer=self.footer, focus_part='header')

        self.i = 1

    def FoolLoader(self, params={}):

        dados = {}
        info = {}
        # dados[a.tid] = {'tid': a.tid, 'dbid': a.id, 'nome': a.nome, 'pai': a.tid, 'level': 0}

        return dados, info

    def load(self):
        dados, info = self.loader({'tab': self.tab, 'ltab': self.ltab, 'search': self.search, 'tree': self.tree})

        self.listbox.dados = dados

        self.i = self.i + 1

        self.fn = FirstNode(nome=self.search, dados=dados)
        self.tw.set_focus(self.fn)


    def update(self, txtbox, changedtext):
        self.search = changedtext
        self.load()


    def unhandled_input(self, k):
        # # update display of focus directory
        if (k == 'f5'):
            x = self.tw.get_next(self.tw.get_focus()[1])[0]
            logging.debug(x.__class__.__name__)
            self.tw.set_focus(x)
            return True
        if (k == 'esc'):
            self._widgetsession.UnShowWidget()
            return

        if (k == 'enter'):
            self._widgetsession.UnShowWidget()
            return



        #raise urwid.ExitMainLoop()
        return False

    def Show(self, _widgetpai, isdialog=False):
        bodyWithInfo = self.view
        headBodyFootFrame = nisk.widgets.LineBox(bodyWithInfo, title='|** Selecionar **|')

        bkg = urwid.AttrWrap(headBodyFootFrame, 'PopupMessageBg')
        over = urwid.Overlay(bkg, self._widgetsession.mainframe.body,
                             ('fixed left', 8, 50),
                             ('fixed top', 8, 25))

        self.load()
        if isdialog:
            lck = threading.Lock()
            self._widgetsession.ShowDialogWidget(over, self.unhandled_input, lck, _widgetpai)
            nisk.util.espera(lck)
        else:
            self._widgetsession.ShowDialogWidget(over, self.unhandled_input, None, _widgetpai, isDialog=False)

#######
# global cache of widgets
_widget_cache = {}


def add_widget(cod, widget):
    _widget_cache[cod] = widget
