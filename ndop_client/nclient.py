#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import curses
import websocket
import json
import argparse
import logging
import logging.handlers


# CONST
DEF_ADDR = "127.0.0.1:9000"
LOG_FILE = "./clientlog"
MENU_WIDTH = 30

CURSES_FOLLOW_WIN_SIZE = -1

__description__ = "NDOP client"
__version__ = "0.0.1"


# --------------------------------
# Shared value
class SharedValue():

    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.l_listener = list()

    def update(self):
        for f in self.l_listener:
            f(self.value)

    def add_listener(self, func):
        self.l_listener.append(func)


# --------------------------------
# Curses functions and class
class CursesPadManager():

    def __init__(self, screen, screen_y, screen_x, height, width, *args, **kwargs):
        self.screen = screen

        self.pos_in_pad_y = 0
        self.pos_in_pad_x = 0

        self.pos_in_screen_y = screen_y
        self.pos_in_screen_x = screen_x

        self.height_in_screen = height
        self.width_in_screen = width

        self.pad = curses.newpad(self.get_view_height(), self.get_view_width())

        self.init(*args, **kwargs)
        self.update()

    def get_view_height(self):
        if self.height_in_screen == CURSES_FOLLOW_WIN_SIZE:
            return max(self.screen.getmaxyx()[0] - self.pos_in_screen_y, 1)
        else:
            return self.height_in_screen

    def get_view_width(self):
        if self.width_in_screen == CURSES_FOLLOW_WIN_SIZE:
            return max(self.screen.getmaxyx()[1] - self.pos_in_screen_x, 1)
        else:
            return self.width_in_screen

    def init(self):
        pass

    def refresh(self):
        height, width = self.screen.getmaxyx()

        if self.pos_in_screen_y < height and self.pos_in_screen_x < width \
                and self.pos_in_screen_y >= 0 and self.pos_in_screen_x >= 0:
            max_posy = min(height, self.pos_in_screen_y + self.get_view_height()) - 1
            max_posx = min(width, self.pos_in_screen_x + self.get_view_width()) - 1
            if self.pos_in_screen_y <= max_posy and self.pos_in_screen_x <= max_posx:
                self.pad.refresh(
                    self.pos_in_pad_y, self.pos_in_pad_x,
                    self.pos_in_screen_y, self.pos_in_screen_x,
                    max_posy, max_posx)
                return
        logger = logging.getLogger()
        logger.warning("Cannot display")

    def set_posinscreen(self, y, x):
        self.pos_in_screen_y = y
        self.pos_in_screen_x = x

    def set_posinpad(self, x, y):
        self.pos_in_pad_y = y
        self.pos_in_pad_x = x

    def move_posinpad(self, dx, dy):
        self.pos_in_pad_y += dy
        if self.pos_in_pad_y < 0:
            self.pos_in_pad_y = 0
        self.pos_in_pad_x += dx
        if self.pos_in_pad_x < 0:
            self.pos_in_pad_x = 0

    def win_resize(self):
        self.pad.resize(self.get_view_height(), self.get_view_width())
        self.update()

    def update(self):
        pass

    def exec_in_pad(self, posy, posx, func, *args, **kwargs):
        height, width = self.pad.getmaxyx()
        if posy < height and posx < width and posy >= 0 and posx >= 0:
            try:
                func(posy, posx, *args, **kwargs)
            except curses.error:
                logger = logging.getLogger()
                logger.debug("Function error on y:%i, x:%i" % (posy, posx))
        else:
            logger = logging.getLogger()
            logger.debug("Invalid pad position y:%i, x:%i" % (posy, posx))
            return False


class CursesMenu(CursesPadManager):

    def init(self, shared_menupos, elem=list()):
        self.elem = elem
        self.shared_menupos = shared_menupos
        self.shared_menupos.add_listener(self.new_menu_value)

    def next(self):
        if self.shared_menupos.value < len(self.elem) - 1:
            self.shared_menupos.value += 1
            self.shared_menupos.update()

    def prev(self):
        if self.shared_menupos.value > 0:
            self.shared_menupos.value -= 1
            self.shared_menupos.update()

    def new_menu_value(self, val):
        self.update()

    def update(self):
        dpos = 5
        cnt = 0
        for elem in self.elem:
            if cnt == self.shared_menupos.value:
                self.exec_in_pad(cnt + dpos, 1, self.pad.addstr, elem[
                                 0:self.get_view_width() - 2], curses.color_pair(1))
            else:
                self.exec_in_pad(cnt + dpos, 1, self.pad.addstr, elem[0:self.get_view_width() - 2])
            cnt += 1

        self.pad.border(2, curses.ACS_VLINE, 1, 1, 1, 1, 1)


class CursesInfo(CursesPadManager):

    def init(self):
        self.nb_refresh = 0

    def update(self):
        self.nb_refresh += 1
        h, w = self.screen.getmaxyx()
        data = "width : %i - height : %i - refresh : %i" % (w, h, self.nb_refresh)

        self.set_posinscreen(h - 1, 0)

        self.exec_in_pad(0, 0, self.pad.addstr, data[0:self.screen.getmaxyx()[1] - 1])


class CursesContent(CursesPadManager):

    def init(self, shared_menupos, l_proto):
        self.menu_pos = shared_menupos.value
        shared_menupos.add_listener(self.new_menu_value)
        self.proto = l_proto

    def new_menu_value(self, val):
        self.menu_pos = val
        self.update()

    def update(self):
        h, w = self.screen.getmaxyx()
        data = "Menu : %i" % (self.menu_pos)

        self.exec_in_pad(0, 0, self.pad.addstr, data)


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
        # argument parser
        args = parser().parse_args()

        # Get logger
        logger = logging.getLogger()

        if args.debug:
            logger.setLevel(logging.DEBUG)

        try:
            self.l_proto = get_list(args.addr)
            self.l_proto = sorted(self.l_proto)
        except:
            print "Cannot get protocols list"
            raise
            return 0
        try:
            # initialisation
            self.curses_init()
            self.color_init()
            self.element_init()

            while not self.term:
                self.check_resize()
                self.screen.refresh()

                # Elements
                self.menu.refresh()

                # Content
                self.content.refresh()

                # INFO
                self.info.update()
                self.info.refresh()

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

    def check_resize(self):
        height, width = self.screen.getmaxyx()

        if height != self.height or width != self.width:
            logger = logging.getLogger()
            logger.debug("Window resize : height: %i, width: %i" % (height, width))
            self.height, self.width = height, width

            for elem in self.l_resize_func:
                elem()

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

        # VAR
        self.height, self.width = self.screen.getmaxyx()
        self.l_resize_func = list()
        self.shared_menupos = SharedValue("menu_pos", 0)

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
        self.info = CursesInfo(self.screen, 0, 0, 1, CURSES_FOLLOW_WIN_SIZE)
        self.l_resize_func.append(self.info.win_resize)

        self.menu = CursesMenu(
            self.screen, 0, 0, CURSES_FOLLOW_WIN_SIZE, MENU_WIDTH, self.shared_menupos, self.l_proto)
        self.l_resize_func.append(self.menu.win_resize)

        self.content = CursesContent(
            self.screen, 0, MENU_WIDTH + 1, CURSES_FOLLOW_WIN_SIZE, CURSES_FOLLOW_WIN_SIZE, self.shared_menupos, self.l_proto)
        self.l_resize_func.append(self.content.win_resize)


# --------------------------------
# Websocket
def get_list(addr):
    ws = websocket.create_connection("ws://" + addr + "/admin")
    result = json.loads(ws.recv())
    ws.close()
    return result["l_protocols"]


# "Sec-WebSocket-Protocol:bandwidth"


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
    parser.add_argument("-d", "--debug", action='store_true', help="debug mode")
    parser.add_argument('--version', action='version', version=('NDOP %s' % __version__))
    return parser


# --------------------------------
# Logger
def conf_logger(debug=False, p_file=None):
    # Set debug mode or not
    if debug:
        mod = logging.DEBUG
    else:
        mod = logging.INFO

    # Get logger
    logger = logging.getLogger()
    logger.setLevel(mod)

    if p_file is not None:
        # Log in a file
        file_handler = logging.handlers.RotatingFileHandler(p_file, 'a', 1000000)
        file_formatter = logging.Formatter('[%(levelname)s] : %(asctime)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)


# --------------------------------
# main function and loop
def main():
    conf_logger(debug=False, p_file=LOG_FILE)

    window = CursesWindow()

    try:
        window.run()
    except KeyboardInterrupt:
        pass

    return 0

if __name__ == "__main__":
    sys.exit(main())
