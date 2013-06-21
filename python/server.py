#encoding: utf-8

"""
Network Display On Pi
NDOP

@author: Olivier BLIN
"""

import sys, os, json, exceptions
import argparse, cmd, time

import config.server

import core.sniffer, core.wsserver
import core.netmod_manager

__program__ = "NDOP"
__version__ = "0.1.0"
__description__ = "Network Sniffer with web display"


class ServerArgumentParser(argparse.ArgumentParser):
    """
    Argument Parser
    """
    
    def __init__(self):
        super(ServerArgumentParser, self).__init__()
        
        # init
        self.description = "%s Version %s" % (__description__, __version__)
        

        self.add_argument("-p", "--port", default=config.server.websocket_port, type=int, dest="websocket_port", 
            help="Websocket server port (default: %i)" % config.server.websocket_port)

        self.add_argument("-i", "--interface", default=config.server.sniffer_device, dest="sniffer_device", 
            help="Network device for sniffing (default: %s)" % config.server.sniffer_device)

        self.add_argument("-m", "--mask", default=config.server.sniffer_device_mask, dest="sniffer_mask", 
            help="Local network mask (default: %s)" % config.server.sniffer_device_mask)

        self.add_argument("-n", "--net", default=config.server.sniffer_device_net, dest="sniffer_net", 
            help="Local network address (default: %s)" % config.server.sniffer_device_net)


def main():
    """
    Main server function

    Stand by Loop
    Modules loader
    """
    
    # Get command line arguments
    args = ServerArgumentParser().parse_args()


    print __description__
    print "------------------------------"

    # Init websocket server (tornado)
    ws = core.wsserver.WsServer(args.websocket_port)
    # init packet capture system
    sniff = core.sniffer.Sniffer(args.sniffer_device, args.sniffer_net, args.sniffer_mask)

    
    # Load and start modules with Modules manager
    modmanager = core.netmod_manager.NetmodManager(config.server.module_list)
    if len(config.server.module_list) > 0:
        print "------------------------------"

    # Start services
    sniff.start()
    time.sleep(0.5)
    ws.start()
    time.sleep(0.5)
    print "------------------------------"
    
    
    # Loop
    try:
        while 1:
            time.sleep(1)
    except KeyboardInterrupt:
        print "Stopping..."
    finally:
        print "------------------------------"
        ws.stop()
        sniff.stop()
        modmanager.stop()
            
    return 0


if __name__ == "__main__":
    sys.exit(main())