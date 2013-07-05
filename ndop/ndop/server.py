#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Network Display On Pi
NDOP

@author: Olivier BLIN
"""

# Python lib import
import sys
import os
import time
import argparse
import importlib
import logging
import logging.handlers
import datetime as dt

# Project configuration file
from config import server_conf

# Project file import
from core.sniffer import SnifferManager
from core.wsserver import WsServer, ClientsList
from core.daemon import Daemon


__program__ = "NDOP"
__version__ = "0.2.0"
__description__ = "Network Sniffer with web display"


class ServerArgumentParser(argparse.ArgumentParser):
    """
    Argument Parser
    """
    def __init__(self):
        super(ServerArgumentParser, self).__init__()

        # init
        self.description = "%s Version %s" % (__description__, __version__)

        # daemon server command. 'run' to avoid daemon mode
        self.add_argument(choices=['start', 'stop', 'restart', 'status', 'run'],
            dest='daemon_cmd', help="Daemon commands control (use 'run' for consol mode)")

        self.add_argument("-p", "--port",
            default=server_conf.websocket_port, type=int, dest="websocket_port",
            help="Websocket server port (default: %i)" % server_conf.websocket_port)

        self.add_argument("-i", "--interface",
            default=server_conf.sniffer_device, dest="sniffer_device",
            help="Network device for sniffing (default: %s)" % server_conf.sniffer_device)

        self.add_argument("-d", "--debug", action='store_true', help="Pass in debug mode")


class ServeurNDOP(Daemon):
    """
    Main class for NDOP server

    Add demonize function
    """

    def __init__(self, args):
        Daemon.__init__(self,
            server_conf.daemon_pid_file,
            stdin=server_conf.daemon_stdin,
            stdout=server_conf.daemon_stdout,
            stderr=server_conf.daemon_stderr,
            root_dir=server_conf.daemon_root_dir,
            working_dir=server_conf.daemon_working_dir)

        self.args = args

    def run(self):
        """
        Main server function

        Stand by Loop
        """

        # Get logger
        logger = logging.getLogger()

        logger.info(">>>>>>>>>>>>>>>>>>>> Network Sniffer with web display")
        logger.info("# " + dt.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))

        # Init websocket server (tornado)
        ws_serv = WsServer(self.args.websocket_port)
        # Init websocket data
        wsdata = ClientsList()
        add_mod_prot(wsdata, server_conf.modules_list)

        # init packet capture system
        sniff = SnifferManager(dev=self.args.sniffer_device)

        # Start services
        try:
            ws_serv.start()
            time.sleep(0.5)
        except:
            ws_serv.stop()
            exit(2)

        try:
            sniff.start()
        except:
            ws_serv.stop()
            sniff.stop()
            exit(2)

        # Loop
        try:
            while 1:
                time.sleep(1)

        except KeyboardInterrupt:
            logger.info("Stopping...")
        finally:
            # Sniffer stop
            sniff.stop()
            sniff.join()
            # Webserver stop
            ws_serv.stop()
            ws_serv.join()
            logger.info("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
                
        exit(0)


def add_mod_prot(wsdata, llmod):
    """
    Load modules to get protocols list
    """

    if len(llmod) > 0:
        for lmod in llmod:
            for mod in lmod:
                try:
                    # import module
                    module = importlib.import_module("ndop.modules." + mod)

                    # Check module main class
                    getattr(module, "NetModChild")

                    # Create an instance
                    modclass = module.NetModChild()
                    # Add protocol for the webserver
                    wsdata.addProtocol(modclass.protocol)
                except:
                    logger = logging.getLogger()
                    logger.debug("Add module protocol :", exc_info=True)


def conf_logger(args):
    """
    Configure general logger parameters
    """
    # create a file handler
    file_handler = logging.handlers.RotatingFileHandler(server_conf.log_file, 'a', 1000000)
    # output handler
    stdout_handler = logging.StreamHandler(sys.stdout)

    # create a logging format
    file_formatter = logging.Formatter('[%(levelname)s] : %(asctime)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    stdout_formatter = logging.Formatter('[%(levelname)s] -> %(message)s')
    stdout_handler.setFormatter(stdout_formatter)

    # Get logger
    logger = logging.getLogger()

    # Set debug mode or not
    if args.debug:
        mod = logging.DEBUG
    else:
        mod = logging.INFO

    logger.setLevel(mod)
    file_handler.setLevel(mod)
    stdout_handler.setLevel(mod)

    # add the handlers to the logger
    logger.addHandler(file_handler)
    if args.daemon_cmd == 'run':
        logger.addHandler(stdout_handler)


def main():
    """
    main function

    Command reader and ask root
    """
    
    # Be root to access network device
    if os.getuid() != 0:
        print("Need to be root !")
        return 2

    # Get command line arguments
    args = ServerArgumentParser().parse_args()

    # Configure logger
    conf_logger(args)

    # Get daemon class
    daemon_serv = ServeurNDOP(args)

    # arguments management
    if 'start' == args.daemon_cmd:
        daemon_serv.start()
    elif 'stop' == args.daemon_cmd:
        daemon_serv.stop()
    elif 'restart' == args.daemon_cmd:
        daemon_serv.restart()
    elif 'run' == args.daemon_cmd:
        daemon_serv.run()

    return 0


if __name__ == "__main__":
    sys.exit(main())
