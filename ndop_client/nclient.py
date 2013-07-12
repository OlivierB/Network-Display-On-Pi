#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import curses
import websocket
import json
import base64
import argparse


# CONST
DEF_ADDR = "127.0.0.1:9000"
MENU_WIDTH = 30

__description__ = "NDOP client"
__version__ = "0.0.1"


# --------------------------------
# Curses functions and class
class CursesPadManager():

    def __init__(self, screen, screen_x, screen_y, height, width):
        self.pad = curses.newpad(height, width)
        self.screen = screen

        self.pos_in_pad_y = 0
        self.pos_in_pad_x = 0

        self.pos_in_screen_y = screen_y
        self.pos_in_screen_x = screen_x

        self.height = height
        self.width = width

    def refresh(self):

        if self.check_pos_screen(self.pos_in_screen_y, self.pos_in_screen_x):
            height, width = self.screen.getmaxyx()
            max_posy = min(height, self.pos_in_screen_y + self.height) - 1
            max_posx = min(width, self.pos_in_screen_x + self.width) - 1
            if self.pos_in_screen_y < max_posy and self.pos_in_screen_x < max_posx:
                self.pad.refresh(
                    self.pos_in_pad_y, self.pos_in_pad_x,
                    self.pos_in_screen_y, self.pos_in_screen_x,
                    max_posy, max_posx)

    def resize(self, height, width):
        pass

    def update(self):
        pass

    def check_pos_screen(self, posy, posx):
        height, width = self.screen.getmaxyx()
        if posy < height and posx < width and posy >= 0 and posx >= 0:
            return True
        else:
            return False

    def check_pos_pad(self, posy, posx):
        height, width = self.pad.getmaxyx()
        if posy < height and posx < width and posy >= 0 and posx >= 0:
            return True
        else:
            return False


class CursesMenu(CursesPadManager):

    def __init__(self, elem=list(), *args, **kwargs):
        CursesPadManager.__init__(self, *args, **kwargs)
        self.elem = elem
        self.pos = 0

        self.update()

    def next(self):
        self.pos += 1
        if self.pos >= len(self.elem):
            self.pos = len(self.elem) - 1
        self.update()

    def prev(self):
        self.pos -= 1
        if self.pos < 0:
            self.pos = 0
        self.update()

    def update(self):
        dpos = 5
        cnt = 0
        for elem in self.elem:
            if self.check_pos_pad(cnt + dpos, 1):
                if cnt == self.pos:
                    self.pad.addstr(cnt + dpos, 1, elem[0:self.width - 2], curses.color_pair(1))
                else:
                    self.pad.addstr(cnt + dpos, 1, elem[0:self.width - 2])
            cnt += 1

        h, w = self.screen.getmaxyx()
        for i in range(h):
            if self.check_pos_pad(i, self.width - 1):
                self.pad.addch(i, self.width - 1, 'I')


class CursesWindow():

    """
    Curses main window
    display management
    keybord management
    """

    def __init__(self):
        self.screen = None
        self.term = False

    def run(self):
        args = parser().parse_args()
        try:
            self.l_proto = get_list(args.addr)
            self.l_proto = sorted(self.l_proto)
        except:
            print "Cannot get protocols list"
            return 0
        try:
            # initialisation
            self.curses_init()
            self.color_init()
            self.element_init()

            refresh = 0
            while not self.term:
                refresh += 1
                height, width = self.screen.getmaxyx()
                self.screen.refresh()
                # self.screen.border()

                self.menu.refresh()
                # self.screen.vline(0, 29, '|', 50)

                # INFO
                self.screen.addstr(height - 1, 0, "width : %i - height : %i - refresh : %i" % (width, height, refresh))

                # arrange cursor
                self.screen.move(0, 0)
                # block display and wait for keyboard input
                self.keys_handler()
                # Clean screen
                self.screen.erase()

        finally:
            self.curses_end()

        return 0

    def keys_handler(self):
        car = self.screen.getch()
        if car == curses.KEY_UP:
            self.menu.prev()
        elif car == curses.KEY_DOWN:
            self.menu.next()
        elif car == ord('q'):
            self.term = True
        elif car == curses.KEY_HOME:
            pass

    def curses_init(self):
        # init curses
        self.screen = curses.initscr()
        # remove screen print
        curses.noecho()
        # get char without enter keypress
        curses.cbreak()
        # get special keys
        self.screen.keypad(1)
        # set a timeout for getch() en ms
        self.screen.timeout(1000)

    def curses_end(self):
        # reverse init actions and close
        curses.nocbreak()
        self.screen.keypad(0)
        curses.echo()
        curses.endwin()

    def color_init(self):
        # color init
        curses.start_color()
        # create pair
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)

    def element_init(self):
        self.menu = CursesMenu(self.l_proto, self.screen, 0, 0, 100, MENU_WIDTH)


# --------------------------------
# Websocket
def get_list(addr):
    ws = websocket.create_connection("ws://" + addr + "/admin")
    ws.send("")
    result = json.loads(base64.b64decode(ws.recv()))
    ws.close()
    return result


# --------------------------------
# Parser
def parser():
    """
    Create parser class to check input arguments
    """
    parser = argparse.ArgumentParser()
    # init
    parser.description = "%s Version %s" % (__description__, __version__)

    parser.add_argument("protocols", nargs='*', help="select some protocols")
    parser.add_argument("--addr", help="websocket server address", default=("%s" % DEF_ADDR))
    parser.add_argument("--list", action='store_true', help="Protocols list")
    parser.add_argument('--version', action='version', version=('NDOP %s' % __version__))
    return parser


# --------------------------------
# main function and loop
def main():
    window = CursesWindow()

    try:
        window.run()
    except KeyboardInterrupt:
        pass

    return 0

if __name__ == "__main__":
    sys.exit(main())
