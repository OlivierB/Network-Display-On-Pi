#encoding: utf-8

"""
Network Display On Pi
NDOP

"""

import sys, os, json
import argparse, cmd, time

import config.server

import core.sniffer, core.wsserver, core.monitoring


__program__ = "NDOP"
__version__ = "0.2"
__description__ = "Network Sniffer with web display"


class ServerArgumentParser(argparse.ArgumentParser):
    """
    Argument Parser
    """
    
    def __init__(self):
        super(ServerArgumentParser, self).__init__() # appel constructeur parent
        
        # initialisations
        self.description = "%s Version %s" % (__description__, __version__)
        
        # ajout des paramètres de lancement
        
        # # test à lancer
        # self.add_argument('bench_test', nargs="?", 
        #     help="test de benchmark a lancer (exemple: example), optionnel si -c est renseigne")
        # # lancement en sous shell
        # self.add_argument("-s", "--shell", action="store_true", dest="shell", 
        #     help="lance la ligne de commande en mode interactif, ignore l'argument bench_test")
        # # paramétrage version fs
        # self.add_argument("-v", "--version", dest="version",
        #     help="parametrage de la version du fs")
        # port d'envoi du serveur aux clients
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

    # Init
    ws = core.wsserver.WsServer()
    m = core.monitoring.Monitoring()
    pcap = core.sniffer.Sniffer()
    cl = core.wsserver.ClientsList()

    # Service start
    m.start()
    pcap.start()
    ws.start()
    
    

    # Loop
    try:
        while 1:
            time.sleep(1)
            val = m.getState()
            cl.send(None, val)
    except KeyboardInterrupt:
        print "Stopping..."
    finally:
        ws.stop()
        m.stop()
        pcap.stop()

            
    return 0

     
if __name__ == "__main__":
    sys.exit(main())