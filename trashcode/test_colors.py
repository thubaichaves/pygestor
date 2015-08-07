# -*- coding: utf-8 -*-

import sys, codecs, locale
locale.setlocale(locale.LC_ALL, '')
sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)

from unicurses import *

import locale
import time

'''''

code = locale.getpreferredencoding()
print sys.stdout.encoding
line = u"XXXÇÃÉÓ ç ã é\n"#.encode('utf-8')
print type(line), len(line)
sys.stdout.write(line);
print line
'''''

def print_in_middle(win, starty, startx, width, string):
    if (win == None): win = stdscr
    y, x = getyx(win)
    if (startx != 0): x = startx
    if (starty != 0): y = starty
    if (width == 0): width = 80
    length = len(string)
    temp = (width - length) / 2
    x = startx + int(temp)
    mvaddstr(y, x, string)

locale.setlocale(locale.LC_ALL, '')
stdscr = initscr()
noecho()
LINES, COLS = getmaxyx(stdscr)

if (has_colors() == False):
    endwin()
    print(u"Your terminal does not support color!")
    exit(1)

start_color()
init_pair(1, COLOR_RED, COLOR_BLACK)

border()
attron(COLOR_PAIR(1))
code = locale.getpreferredencoding()
print_in_middle(stdscr, int(LINES / 2), 0, 0, u"This  should be displayed in red color.ç ã é \N{BULLET}".encode('850',errors='replace'))
# print_in_middle(stdscr, int(LINES / 2), 0, 0, CSTR( u"This  should be displayed in red color.ããéç "))
attroff(COLOR_PAIR(1))
getch()
endwin()
''''''
print code