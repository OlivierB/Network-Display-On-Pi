#encoding: utf-8

"""
Network Display On Pi
NDOP

@author: Olivier BLIN
"""

import sys, os, json, exceptions
import argparse, cmd, time
import importlib

import config.server

import core.sniffer, core.wsserver, core.monitoring
import core.update

# import core.netmod_bandwidth, core.netmod_top

MODULE_LIST = ["netmod_bandwidth", "netmod_top"]

__program__ = "NDOP"
__version__ = "0.2"
__description__ = "Network Sniffer with web display"


class ServerArgumentParser(argparse.ArgumentParser):
    """
    Argument Parser
    """
    
    def __init__(self):
        super(ServerArgumentParser, self).__init__()
        
        # initialisations
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
    
    """
    
    args = ServerArgumentParser().parse_args()


    print __description__
    print "------------------------------"

    # Init
    ws = core.wsserver.WsServer(args.websocket_port)
    sniff = core.sniffer.Sniffer(args.sniffer_device, args.sniffer_net, args.sniffer_mask)

    # Webserver data
    wsdata = core.wsserver.ClientsList()

    # Service start
    sniff.start()
    time.sleep(0.5)
    ws.start()
    time.sleep(0.5)
    print "------------------------------"
    modlist = load_modules(MODULE_LIST, sniff, wsdata)
    if len(MODULE_LIST) > 0:
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
        stop_modules(modlist)
            
    return 0

     
def load_modules(lmod, sniffer, ws):
    lLoadMod = list()
    for m in lmod:
        try:
            # import module
            module = importlib.import_module("core." + m)

            # Check module main class
            getattr(module, "MyMod")

            # Create an instance
            modclass = module.MyMod(sniffer, websocket=ws)
            # start module
            modclass.start()

            # add module to the list
            lLoadMod.append((module, modclass))
            print "Start module", m

            # except ImportError as e:
            #     print m, ":", e
            # except AttributeError as e:
            #     print m, ":", e
        except Exception as e:
            print m, ":", e

    return lLoadMod


def stop_modules(lmod):
    for m in lmod:
        m[1].stop()

if __name__ == "__main__":
    sys.exit(main())