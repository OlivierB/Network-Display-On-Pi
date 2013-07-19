#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Network Display On Pi
NDOP

entry-point : main()

@author: Olivier BLIN
"""

# Python lib import
import sys
import time
import logging
import signal
import datetime as dt

# Project file import
from core.sniffer import SnifferManager
from core.wsserver import WsServer, WsData
from core.daemon import Daemon
from core.configCenter import ConfigChecker, ConfigCenter


RUN = True


def handler_int(signum, frame):
    global RUN
    RUN = False


def ndop_run(config):
    """
    Main server function

    waiting Loop
    """

    # Get logger
    logger = logging.getLogger()

    logger.info(">>>>>>>>>>>>>>>>>>>> Network Sniffer with web display")
    logger.info("# " + dt.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))

    # Init websocket server (tornado)
    ws_serv = WsServer(config.ws_port)
    # Init websocket data
    wsdata = WsData()
    # Add authorized protocols in websocket data
    wsdata.addListProtocols(config.l_protocols)

    # init packet capture system
    sniff = SnifferManager(config)

    try:
        signal.signal(signal.SIGINT, handler_int)

        # Start services
        ws_serv.start()
        time.sleep(0.5)
        sniff.start()

        # Loop
        while RUN:
            time.sleep(1)

        logger.info("Stopping...")

    finally:
        # Sniffer stop
        sniff.stop()
        if sniff.is_running:
            sniff.join()

        # Webserver stop
        ws_serv.stop()
        if ws_serv.is_alive():
            ws_serv.join()
        logger.info("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    return 0


def main():
    """
    main function
    """
    # Gather and check conf
    conf = ConfigChecker()
    try:
        conf.config_checker()
    except ConfigCenter as e:
        if (conf.daemon and conf.debug) or not conf.daemon:
            sys.stderr.write("Config Cheker : %s\n" % e)
        return 2

    # Launch program in normal mode or daemon mode
    if conf.cmd == "test":
        pass
    elif conf.cmd == "daemon":
        daemon_serv = Daemon(
            conf.daemon_pid_file,
            function=ndop_run, args=(conf,),
            stdout=conf.daemon_stdout,
            stderr=conf.daemon_stderr)
        daemon_serv.start()

    elif conf.cmd == "run":
        return ndop_run(conf)

    return 0
    

if __name__ == "__main__":
    sys.exit(main())
