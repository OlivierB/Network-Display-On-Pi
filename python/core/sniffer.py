#encoding: utf-8

"""
Client system sniffer

Use pcap

@author: Olivier BLIN
"""

import config.server

import sys, time, socket, types
import string, struct, operator
import importlib
import multiprocessing as mp
import pcap

import core.network_callback
import core.network_utils
import core.packet

PCAP_PROMISCUOUS_MODE   = 1
PCAP_SNIFFER_TIMEOUT    = 300
MIN_TIME_MOD_UPDATE     = 0.5




class Sniffer(mp.Process):
    """
    Class for packet capture

    This class some modules which analyse packets and make stats
    """
    number = 0
    def __init__(self, pipe, dev="eth0"):
        mp.Process.__init__(self)

        # stop condition
        self.Terminated = mp.Value('i', 0)

        # Var
        self.dev = dev
        self.pipe = pipe

    def stop(self):
        self.Terminated.value = 1

    def run(self):
        print "Sniffer : Capture start"
        # Init
        term = self.Terminated.value    # little optimisation (local variable)
        pipe = self.pipe
        lmod = load_mod(config.server.module_list)
        tb = time.time()

        # Protocols
        wsdata = core.wsserver.ClientsList()
        for m in lmod:
            wsdata.addProtocol(m.get_protocol())

        # Get device informations if possible (IP address assigned)
        try:
            net, mask = pcap.lookupnet(dev)
        except:
            net, mask = "192.168.1.0", "255.255.255.0"

        # Create new pcap capture object
        p = pcap.pcapObject()
        # (Dev, buffer, promiscuous mode, timeout)
        p.open_live(self.dev, 1600, PCAP_PROMISCUOUS_MODE, PCAP_SNIFFER_TIMEOUT)


        try:    
            # Handler loop
            while not term:
                pkt = p.next()

                if pkt != None:
                    # Decode packet
                    pktdec = core.network_utils.packet_decode(pkt[0], pkt[1], pkt[2])
                    # pktdec = core.packet.Packet(pkt[0], pkt[1], pkt[2])

                    # send pkt to modules
                    for m in lmod:
                        m.pkt_handler(pktdec)

                # Module update
                if time.time() - tb > MIN_TIME_MOD_UPDATE:
                    tb = time.time()
                    ls = list()
                    for m in lmod:
                        data = m.get_data()
                        if data != None:
                            ls.append((m.get_protocol(), data))
                    if len(ls) > 0:
                        pipe.send(ls)                    


        except KeyboardInterrupt:
            # End
            print "Sniffer : Stopping..."
            a, b, c = p.stats()
            print 'Sniffer : %d packets received, %d packets dropped, %d packets dropped by interface -' % p.stats(), b/(a*1.0+1)*100
        except Exception as e:
            print "Sniffer : ", e
            raise



        

def load_mod(lmod):
        """
        Load modules
        """
        # Singeton Webserver data (for websocket)
        l_modules = list()

        if len(lmod) > 0:
            print "------------------------------"
            for m in lmod:
                try:
                    # import module
                    module = importlib.import_module("modules." + m)

                    # Check module main class
                    getattr(module, "NetModChild")

                    # Create an instance
                    modclass = module.NetModChild()

                    # add module to the list
                    l_modules.append(modclass)
                    print "Load module", m

                    # except ImportError as e:
                    #     print m, ":", e
                    # except AttributeError as e:
                    #     print m, ":", e
                except Exception as e:
                    print m, ":", e
            print "------------------------------"

        return l_modules