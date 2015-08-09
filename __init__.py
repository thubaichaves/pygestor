#!/usr/bin/python
# -*- coding: utf-8 -*-



import nisk
import urwid
import locale
import logging
import appbase
import app

if __name__ == '__main__':
    try:

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
        
    except Exception, e:
        logging.exception(e)