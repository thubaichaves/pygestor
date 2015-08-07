#!/usr/bin/python
# -*- coding: utf-8 -*-

import nisk
import appbase
import app
import urwid
import locale
import logging

# if __name__ == '__main__':
# try:


#urwid.set_encoding("cp850")
locale.setlocale(locale.LC_ALL, "")
urwid.set_encoding("UTF-8")
nisk.util.TerminalLogger.setup()
logging.debug('''
.
.
*************************************
*****   INICIO               ********
*************************************
.
.
''')
app.app.Inicia()

# except:
# #raise urwid.ExitMainLoop()
#     pass