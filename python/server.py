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
        

        self.add_argument("-p", "--port", default=9000, type=int, dest="port", 
            help="Websocket server port (default: %i)" % 9000)

        self.add_argument("-m", "--mask", default="255.255.255.0", dest="mask", 
            help="Local network mask (default: 255.255.255.0)")

        self.add_argument("-n", "--net", default="192.168.1.0", dest="net", 
            help="Local network address (default: 192.168.1.0)")



def main():
    """
    
    """
    
    args = ServerArgumentParser().parse_args()


    print __description__
    print "------------------------------"

    # Init
    ws = core.wsserver.WsServer()
    m = core.monitoring.Monitoring()
    pcap = core.sniffer.Sniffer()

    cl = core.wsserver.ClientsList()
    u = core.update.Update(m, pcap)

    # Service start
    m.start()
    time.sleep(0.5)
    pcap.start()
    time.sleep(0.5)
    ws.start()
    time.sleep(0.5)
    print "------------------------------"
    
    

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
        pcap.stop()

            
    return 0

     
if __name__ == "__main__":
    sys.exit(main())