#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import curses
import pprint
import websocket
import json
import argparse
import logging
import logging.handlers
from threading import Thread


# CONST
DEF_ADDR = "127.0.0.1:9000"
LOG_FILE = "./clientlog"
MENU_WIDTH = 30
GETCH_TIMEOUT = 200

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

    def init(self, shared_menupos, subp_manager, l_protocols):
        self.menu_pos = shared_menupos.value
        shared_menupos.add_listener(self.new_menu_value)
        self.subp_manager = subp_manager
        self.l_protocols = l_protocols

        self.subp_manager.add_listener(self.new_wsdata)

    def new_menu_value(self, val):
        self.menu_pos = val
        self.update()

    def new_wsdata(self, name):
        if self.l_protocols[self.menu_pos] == name:
            self.update()

    def update(self):
        self.pad.erase()
        h, w = self.screen.getmaxyx()
        data = "Menu : %i" % (self.menu_pos)

        self.exec_in_pad(0, 0, self.pad.addstr, data)
        self.exec_in_pad(1, 0, self.pad.addstr, "Protocol :" +
                         self.subp_manager.l_subp_handler[self.menu_pos].subprotocol)

        stt = 2
        data = self.subp_manager.l_subp_handler[self.menu_pos].get_format(h, w)
        for line in data.split("\n"):
            self.exec_in_pad(stt, 0, self.pad.addstr, line)
            stt += 1


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

        # Try to get protocols list
        try:
            self.l_proto = get_list(args.addr)
            self.l_proto = sorted(self.l_proto)
        except:
            print "Cannot get protocols list"
            return 0

        # Websockets manager
        self.ws_manager = Websocket_manager(args.addr, self.l_proto)

        try:
            # initialisation
            self.curses_init()
            self.color_init()
            self.element_init()

            # WS listen
            self.ws_manager.start()

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
            # stop subprotocols handler
            self.ws_manager.stop()

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
        self.screen.timeout(GETCH_TIMEOUT)

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
            self.screen, 0, MENU_WIDTH + 1, CURSES_FOLLOW_WIN_SIZE, CURSES_FOLLOW_WIN_SIZE, self.shared_menupos, self.ws_manager, self.l_proto)
        self.l_resize_func.append(self.content.win_resize)


# --------------------------------
# Websocket
def get_list(addr):
    ws = websocket.create_connection("ws://" + addr + "/admin")
    result = json.loads(ws.recv())
    ws.close()
    return result["l_protocols"]


class Websocket_manager():

    def __init__(self, addr, l_protocols):
        self.l_protocols = l_protocols
        self.addr = addr
        self.listen = list()
        # Create handlers for subprotocols
        self.l_subp_handler = list()
        for p in self.l_protocols:
            if p in list_handle_subprotocols.keys():
                self.l_subp_handler.append(list_handle_subprotocols[p](self, self.addr, p))
            else:
                self.l_subp_handler.append(Websocket_handler(self, self.addr, p))

    def start(self):
        # start
        for subp in self.l_subp_handler:
            subp.start()

    def stop(self):
        # start
        for subp in self.l_subp_handler:
            subp.stop()

    def trigger(self, subprotocol):
        for elem in self.listen:
            elem(subprotocol)

    def add_listener(self, func):
        self.listen.append(func)


class Websocket_handler(Thread):

    """
    Thread class to handle one websocket subprotocol
    """

    def __init__(self, manager, addr, subprotocol):
        Thread.__init__(self)

        self.manager = manager
        self.addr = addr
        self.subprotocol = subprotocol
        self.ws = None
        self.connect = True
        self.last = ""

    def run(self):

        try:
            self.ws = websocket.create_connection("ws://" + self.addr + "/", header=[
                                                  "Sec-WebSocket-Protocol:" + self.subprotocol])
            self.connect = True
        except:
            self.connect = False
            pass

        try:
            while self.connect:
                recv = self.ws.recv()
                try:
                    decoded = json.loads(recv)
                    self.handle_data(decoded)
                    self.manager.trigger(self.subprotocol)
                except:
                    pass
        except:
            self.connect = False

        return 0

    def handle_data(self, data):
        pp = pprint.PrettyPrinter(indent=2, width=100, depth=None, stream=None)
        self.last = pp.pformat(data)

    def get_format(self, height, width):
        return self.last

    def stop(self):
        self.connect = False
        if self.ws is not None:
            self.ws.close()


class Websocket_subprotocol_bandwidth(Websocket_handler):
    pass

list_handle_subprotocols = {
    "bandwidth": Websocket_subprotocol_bandwidth
}


# --------------------------------
# Parser
def parser():
    """
    Create parser class to check input arguments
    """
    parser = argparse.ArgumentParser()
    # init
    parser.description = "%s Version %s" % (__description__, __version__)

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
