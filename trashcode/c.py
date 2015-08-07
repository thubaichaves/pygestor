#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import unicurses as curses
from  unicurses import *

import locale
import time
locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

x  = initscr()
curses.noecho() 
curses.curs_set(0) 
#stdscr.keypad(1)
#c=screen.get_wch()
#screen.addch(c)

x.addstr("This çis ´´ ´´ `` a Sample Curses Script\n\n")
#stdscr.addstr("This çis ´´ ´´ `` a Sample Curses Script\n\n")
while True: 
   event = stdscr.getch() 
   if event == ord("q"): break 
    
curses.endwin()
print code
