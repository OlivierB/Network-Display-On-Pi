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
LOG_FILE = "/tmp/clientlog"
MENU_WIDTH = 30
GETCH_TIMEOUT = 200

CURSES_FOLLOW_WIN_SIZE = -1

__description__ = "NDOP client"
__version__ = "0.0.2"


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


class CursesContent_handler(CursesPadManager):

    def init(self, ws):
        
        self.ws = ws


    def update(self):
        self.pad.erase()
        h, w = self.screen.getmaxyx()

        self.exec_in_pad(0, 0, self.pad.addstr, "Protocol : %s" % self.ws.subprotocol)

        stt = 2
        data = self.ws.get_format()
        for line in data.split("\n"):
            self.exec_in_pad(stt, 0, self.pad.addstr, line)
            stt += 1


class CursesContent_handler_bandwidth(CursesContent_handler):
    def update(self):
        self.pad.erase()
        h, w = self.screen.getmaxyx()

        self.exec_in_pad(0, 0, self.pad.addstr, "Protocol : %s - Page : %i" %
                         (self.ws.subprotocol, self.ws.page))

        

        data = self.ws.get_format()
        if data is None:
            return

        if self.ws.page >= 4:
            self.exec_in_pad(2, 0, self.pad.addstr, "Empty" , curses.color_pair(1))
            return

        stt = 2
        if self.ws.page == 0:
            l_elem = ["tot_out_Ko", "tot_in_Ko", "loc_Ko", "in_Ko", "out_Ko", "Ko"]
            for k in l_elem:
                try:
                    self.exec_in_pad(stt, 0, self.pad.addstr, k , curses.color_pair(1))
                    self.exec_in_pad(stt, len(k), self.pad.addstr, " -> " + str(data[k]))
                    stt += 2
                except:
                    pass
            self.graph(15, 1, 15, 75, "Ko")
        elif self.ws.page == 1:
            l_elem = ["in_Ko", "out_Ko"]
            for k in l_elem:
                try:
                    self.exec_in_pad(stt, 0, self.pad.addstr, k , curses.color_pair(1))
                    self.exec_in_pad(stt, len(k), self.pad.addstr, " -> " + str(data[k]))
                    stt += 2
                except:
                    pass
                self.graph(10, 1, 15, 75, "in_Ko")
                self.graph(27, 1, 15, 75, "out_Ko")
        elif self.ws.page == 2:
            l_elem = ["tot_in_Ko", "tot_out_Ko"]
            for k in l_elem:
                try:
                    self.exec_in_pad(stt, 0, self.pad.addstr, k , curses.color_pair(1))
                    self.exec_in_pad(stt, len(k), self.pad.addstr, " -> " + str(data[k]))
                    stt += 2
                except:
                    pass
                self.graph(10, 1, 15, 75, "tot_in_Ko")
                self.graph(27, 1, 15, 75, "tot_out_Ko")
        elif self.ws.page == 3:
            l_elem = ["loc_Ko"]
            for k in l_elem:
                try:
                    self.exec_in_pad(stt, 0, self.pad.addstr, k , curses.color_pair(1))
                    self.exec_in_pad(stt, len(k), self.pad.addstr, " -> " + str(data[k]))
                    stt += 2
                except:
                    pass
                self.graph(15, 1, 15, 75, "loc_Ko")

    def graph(self, y, x, h, w, elem):
        space = 2
        if self.ws.data is None:
            return

        mv = 1
        for e in self.ws.data:
            if e[elem] > mv:
                mv = e[elem]

        ratio = h / (mv*1.0)

        pos = len(self.ws.data) - 1
        posw = x + w
        while posw > x and pos >= 0:
            posh = y + h
            while posh > y:
                if ratio * self.ws.data[pos][elem] <= h - (posh-y):
                    break
                else:
                    self.exec_in_pad(posh, posw, self.pad.addstr, "#")
                    posh -= 1

            pos -= 1
            posw -= 1
        self.exec_in_pad(y + h, x + w +space, self.pad.addstr, "-0 Ko")
        for i in range(y+1, y + h):
            self.exec_in_pad(i, x + w +space, self.pad.addstr, "|")
        self.exec_in_pad(y, x + w +space, self.pad.addstr, "-%i Ko" % mv)


class CursesContent_handler_system(CursesContent_handler):
    def update(self):
        self.pad.erase()
        h, w = self.screen.getmaxyx()

        self.exec_in_pad(0, 0, self.pad.addstr, "Protocol : %s" % self.ws.subprotocol)

        data = self.ws.get_format()
        if data is None:
            return

        stt = 2
        for k in ["proc_load", "mem_load", "swap_load"]:
            try:
                self.exec_in_pad(stt, 0, self.pad.addstr, k , curses.color_pair(1))
                self.exec_in_pad(stt, len(k), self.pad.addstr, " -> " + str(data[k])+"%")
                self.draw(stt+1, 0, data[k])
                stt += 3
            except:
                pass
        

    def draw(self, y, x, val):
        self.exec_in_pad(y, x, self.pad.addstr, "[")
        for i in range(1, 21):
            if (i*5) <=  val:
                if val < 33:
                    self.exec_in_pad(y, x+i, self.pad.addstr, "I" , curses.color_pair(2))
                elif val < 66:
                    self.exec_in_pad(y, x+i, self.pad.addstr, "I" , curses.color_pair(3))
                else:
                    self.exec_in_pad(y, x+i, self.pad.addstr, "I" , curses.color_pair(4))

        self.exec_in_pad(y, x+21, self.pad.addstr, "]")



class CursesContent_handler_item(CursesContent_handler):
    def update(self):
        self.pad.erase()
        h, w = self.screen.getmaxyx()

        self.exec_in_pad(0, 0, self.pad.addstr, "Protocol : %s" % self.ws.subprotocol)

        stt = 2
        data = self.ws.get_format()
        if data is None:
            return

        lk = data.keys()

        for k in lk:
            self.exec_in_pad(stt, 0, self.pad.addstr, k , curses.color_pair(1))
            self.exec_in_pad(stt, len(k), self.pad.addstr, " -> " + str(data[k]))
            stt += 2




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


        try:
            # initialisation
            self.curses_init()
            self.color_init()
            self.element_init()

            # Websockets manager
            screen_args = [self.screen, 0, MENU_WIDTH + 1, CURSES_FOLLOW_WIN_SIZE, CURSES_FOLLOW_WIN_SIZE]
            self.ws_manager = Websocket_manager(args.addr, self.l_proto, screen_args)
            self.ws_manager.start()

            while not self.term:
                self.check_resize()
                self.screen.refresh()

                # Elements
                self.menu.refresh()

                # Content
                self.ws_manager.refresh(self.shared_menupos.value)

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
            if self.ws_manager is not None:
                self.ws_manager.stop()

        return 0

    def keys_handler(self):
        car = self.screen.getch()
        if car == curses.KEY_UP:
            self.menu.prev()
        elif car == curses.KEY_DOWN:
            self.menu.next()
        elif car == curses.KEY_RIGHT:
            self.ws_manager.next_page(self.shared_menupos.value)
        elif car == curses.KEY_LEFT:
            self.ws_manager.prev_page(self.shared_menupos.value)
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
        self.shared_pagepos = SharedValue("page_pos", 0)
        self.ws_manager = None

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
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_YELLOW)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLUE)

    def element_init(self):
        self.info = CursesInfo(self.screen, 0, 0, 1, CURSES_FOLLOW_WIN_SIZE)
        self.l_resize_func.append(self.info.win_resize)

        self.menu = CursesMenu(
            self.screen, 0, 0, CURSES_FOLLOW_WIN_SIZE, MENU_WIDTH, self.shared_menupos, self.l_proto)
        self.l_resize_func.append(self.menu.win_resize)
        

# --------------------------------
# Websocket
def get_list(addr):
    ws = websocket.create_connection("ws://" + addr + "/admin")
    result = json.loads(ws.recv())
    ws.close()
    return result["l_protocols"]


class Websocket_manager():

    def __init__(self, addr, l_protocols, screen_args):
        self.l_protocols = l_protocols
        self.addr = addr

        # Create handlers for subprotocols
        self.l_subp_handler = list()

        for p in self.l_protocols:
            if p in list_handle_subprotocols.keys():
                self.l_subp_handler.append(list_handle_subprotocols[p](self, self.addr, p, screen_args))
            else:
                self.l_subp_handler.append(Websocket_handler(self, self.addr, p, screen_args))

    def start(self):
        # start
        for subp in self.l_subp_handler:
            subp.start()

    def stop(self):
        # stop
        for subp in self.l_subp_handler:
            subp.stop()

    def refresh(self, num):
        self.l_subp_handler[num].refresh()

    def next_page(self, num):
        self.l_subp_handler[num].next_page()
        self.l_subp_handler[num].screen_content.update()

    def prev_page(self, num):
        self.l_subp_handler[num].prev_page()
        self.l_subp_handler[num].screen_content.update()


class Websocket_handler(Thread):

    """
    Thread class to handle one websocket subprotocol
    """

    def __init__(self, manager, addr, subprotocol, screen_args=list()):
        Thread.__init__(self)

        self.manager = manager
        self.addr = addr
        self.subprotocol = subprotocol
        self.ws = None
        self.connect = True
        self.last = None
        self.data = list()
        self.page = 0

        sc_args = screen_args + [self]
        self.init_view(sc_args)

    def init_view(self, sc_args):
        self.screen_content = CursesContent_handler(*sc_args)

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
                    self.screen_content.update()
                except:
                    pass
        except:
            self.connect = False

        return 0

    def handle_data(self, data):
        self.last = data

    def get_format(self):
        if self.last is not None:
            pp = pprint.PrettyPrinter(indent=2, width=100, depth=None, stream=None)
            return pp.pformat(self.last)
        else:
            return ""

    def next_page(self):
        self.page += 1

    def prev_page(self):
        if self.page > 0:
            self.page -= 1

    def stop(self):
        self.connect = False
        if self.ws is not None:
            self.ws.close()

    def refresh(self):
        self.screen_content.refresh()


class Websocket_subprotocol_bandwidth(Websocket_handler):
    
    def init_view(self, sc_args):
        self.screen_content = CursesContent_handler_bandwidth(*sc_args)

    def handle_data(self, data):
        self.last = data
        self.data.append(data)
        if len(self.data) > 100:
            self.data.pop(0)

    def get_format(self):
        return self.last


class Websocket_subprotocol_pktloss(Websocket_handler):
    
    def init_view(self, sc_args):
        self.screen_content = CursesContent_handler_item(*sc_args)

    def handle_data(self, data):
        self.last = data

    def get_format(self):
        return self.last


class Websocket_subprotocol_srvstats(Websocket_handler):
    
    def init_view(self, sc_args):
        self.screen_content = CursesContent_handler_system(*sc_args)

    def handle_data(self, data):
        self.last = data

    def get_format(self):
        return self.last


list_handle_subprotocols = {
    "bandwidth": Websocket_subprotocol_bandwidth,
    "packet_loss": Websocket_subprotocol_pktloss,
    "server_stat": Websocket_subprotocol_srvstats
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
