#encoding: utf-8

"""
Network Display On Pi
NDOP

@author: Olivier BLIN
"""

import sys, os, json, exceptions
import argparse, cmd, time, importlib
from multiprocessing import Pipe

import config.server

import core.sniffer, core.wsserver


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


    print "####################################"
    print "# Network Sniffer with web display #"
    print "####################################"

    pipe_receiver, pipe_sender  = Pipe(duplex=False)
    # Init websocket server (tornado)
    ws = core.wsserver.WsServer(args.websocket_port)
    wsdata = core.wsserver.ClientsList()
    add_mod_prot(wsdata, config.server.module_list)
    # print wsdata.getProtocols()
    # init packet capture system
    sniff = core.sniffer.Sniffer(pipe=pipe_sender, dev=args.sniffer_device) # , args.sniffer_net, args.sniffer_mask

    # Start services
    ws.start()
    time.sleep(0.5)
    sniff.start()
    time.sleep(0.5)
    

    # Loop
    try:
        while 1:
            # time.sleep(1)
            recv = pipe_receiver.recv()
            for r in recv:
                wsdata.send(r[0], r[1])
            # print "stats : ", sniff.stats()
    except KeyboardInterrupt:
        print "Stopping..."
    finally:
        print "------------------------------"
        # Sniffer stop
        sniff.stop()
        sniff.join()
        # Webserver stop
        ws.stop()
        ws.join()
            
    return 0


def add_mod_prot(wsdata, lmod):
    """
    Load modules
    """

    if len(lmod) > 0:
        for m in lmod:
            try:
                # import module
                module = importlib.import_module("modules." + m)

                # Check module main class
                getattr(module, "NetModChild")

                # Create an instance
                modclass = module.NetModChild()
                # Add protocol for the webserver
                wsdata.addProtocol(modclass.get_protocol())

            except Exception as e:
                # print e
                raise


if __name__ == "__main__":
    sys.exit(main())