#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Network Display On Pi
NDOP

@author: Olivier BLIN
"""

# Python lib import
import sys
import time
import importlib
import logging
import datetime as dt

# Project file import
from core.sniffer import SnifferManager
from core.wsserver import WsServer, ClientsList
from core.daemon import Daemon
from core.configCenter import ConfigChecker, ConfigCenter


def ndop_run(config):
    """
    Main server function

    Stand by Loop
    """

    # Get logger
    logger = logging.getLogger()

    logger.info(">>>>>>>>>>>>>>>>>>>> Network Sniffer with web display")
    logger.info("# " + dt.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))

    # Init websocket server (tornado)
    ws_serv = WsServer(config.ws_port)
    # Init websocket data
    wsdata = ClientsList()
    for prot in config.l_protocols:
        wsdata.addProtocol(prot)

    # init packet capture system
    sniff = SnifferManager(config)

    # Start services
    try:
        ws_serv.start()
        time.sleep(0.5)
    except:
        ws_serv.stop()
        return 2

    try:
        sniff.start()
    except:
        ws_serv.stop()
        sniff.stop()
        return 2

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
            
    return 0


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


def main():
    """
    main function
    """
    
    # Gather and check conf
    conf = ConfigChecker()
    try:
        conf.config_checker()
    except ConfigCenter as e:
        print "Config Cheker Error : %s" % e

    print "Good"

    # logger = logging.getLogger()
    # logger.info("in main")

    if conf.cmd in ['start', 'restart']:
        daemon_serv = Daemon(
            conf.daemon_pid_file,
            function=ndop_run, args=(conf,), 
            stdout=conf.daemon_stdout, 
            stderr=conf.daemon_stderr)

        if conf.cmd == 'start':
            daemon_serv.start()
        elif conf.cmd == 'restart':
            daemon_serv.restart()

    elif conf.cmd in ['stop', 'status']:
        daemon_serv = Daemon(conf.daemon_pid_file)

        if conf.cmd == 'stop':
            daemon_serv.stop()
        elif conf.cmd == 'status':
            daemon_serv.status()
    elif conf.cmd == 'run':
        return ndop_run(conf)
 
    return 0

if __name__ == "__main__":
    sys.exit(main())
