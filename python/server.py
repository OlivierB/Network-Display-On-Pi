#encoding: utf-8

"""
Network Display On Pi
NDOP

"""

import sys, os
import argparse, cmd, time

import config.server

import core.sniffer


__program__ = "NDOP"
__version__ = "0.1"
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




def main():
    """
    
    """
    
    args = ServerArgumentParser().parse_args()

   
    print __description__

    p = sniffer.Pcap()
    # p.start()

    time.sleep(7)

            
    return 0

     
if __name__ == "__main__":
    sys.exit(main())