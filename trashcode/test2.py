#!/usr/bin/python

import urwid
import urwid.curses_display
import os

ui = urwid.curses_display.Screen()

ui.register_palette([
    ('splash', 'black', 'dark red'),
    ('bg_splash', 'black', 'dark blue'),
    ('header', 'white', 'black'),
    ('footer', 'dark red', 'light gray'),
    ('browser', 'white', 'dark blue'),
    ('selected', 'white', 'dark red'),
    ('file', 'light gray', 'dark blue'),
    ('dir', 'light magenta', 'dark blue')
])


def run():
    size = ui.get_cols_rows()
    inst = pyrun()
    inst.main()


class pyrun:
    def __init__(self):
        try:
            self.items = self.get_file_names(self.cwd)
        except AttributeError:
            self.initial_cwd = os.getcwd()
            self.cwd = self.initial_cwd
            self.items = self.get_file_names(self.cwd)
        self.listbox = urwid.AttrWrap(urwid.ListBox(self.items), 'browser')
        menu_txt = urwid.Text("F1 - Help     F2 - Options     F10 - Quit   Now: % s" % self.cwd)
        header = urwid.AttrWrap(menu_txt, 'header')
        down_txt = urwid.Text("pybrowser. Left Arrow: Parent.")
        footer = urwid.AttrWrap(down_txt, 'footer')
        self.top = urwid.Frame(self.listbox, header, footer)

    def main(self):
        size = ui.get_cols_rows()

        while True:
            self.draw_screen(size)
            keys = ui.get_input()
            if "f10" in keys:
                break
            for k in keys:
                if k == "window resize":
                    size = ui.get_cols_rows()
                    continue
                elif k == "left":
                    self.cwd = os.path.split(self.cwd)[0]
                    self.__init__()
                    continue

    def draw_screen(self, size):
        canvas = self.top.render(size, focus=True)
        ui.draw_screen(size, canvas)

    def get_file_names(self, cwd):
        desc_list = os.listdir(cwd)
        dir_list = []
        file_list = []

        for f in desc_list:
            if os.path.isdir(os.path.join(cwd, f)):
                dir_list.append(f)
            elif os.path.isfile(os.path.join(cwd, f)):
                file_list.append(f)

        file_list = [urwid.AttrWrap(urwid.Text(f), 'file') for f in file_list]
        dir_list = [urwid.AttrWrap(urwid.Text(f), 'dir') for f in dir_list]

        return ( dir_list + file_list )


ui.run_wrapper(run)