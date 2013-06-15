#encoding: utf-8

"""
Network Display On Pi
NDOP

@author: Olivier BLIN
"""

import sys, os, json
import argparse, cmd, time

import config.server

import core.sniffer, core.wsserver, core.monitoring
import core.update


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
    m = core.monitoring.Monitoring()
    sniff = core.sniffer.Sniffer(args.sniffer_device, args.sniffer_net, args.sniffer_mask)

    # Service start
    m.start()
    time.sleep(0.5)
    sniff.start()
    time.sleep(0.5)
    ws.start()
    time.sleep(0.5)
    print "------------------------------"
    
    # Data managememt
    cl = core.wsserver.ClientsList()
    u = core.update.Update(m, sniff)
    

    # Loop
    try:
        while 1:
            time.sleep(1)
            val = m.getState()
            # print cl.getData().keys()
            u.update()
    except KeyboardInterrupt:
        print "Stopping..."
    finally:
        print "------------------------------"
        ws.stop()
        m.stop()
        sniff.stop()

            
    return 0

     
if __name__ == "__main__":
    sys.exit(main())