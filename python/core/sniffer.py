#encoding: utf-8

"""
Client system sniffer

Use pcap

@author: Olivier BLIN
"""

import pcap
import sys
import string
import time
import threading
import socket
import struct
import types

import core.network_utils

PCAP_PROMISCUOUS_MODE=1

class Sniffer(threading.Thread):
    """
    
    """

    def __init__(self, dev="eth0", net="192.168.1.0", mask="255.255.255.0"):
        threading.Thread.__init__(self)
        # stop condition
        self.Terminated = False

        # param
        self.dev = dev
        self.net = net
        self.mask = mask

        # Create new pcap capture object
        self.p = pcap.pcapObject()

        # Stat


    def run(self):

        print "Sniffer : Pcap start on %s..." % self.dev

        time.sleep(1.5)

        try:
            # Get device informations if possible (IP address assigned)
            try:
                net, mask = pcap.lookupnet(self.dev)
                self.net = pcap.ntoa(net)
                self.mask = pcap.ntoa(mask)
            except:
                pass

            # (Dev, buffer, promiscuous mode, timeout)
            self.p.open_live(self.dev, 1600, PCAP_PROMISCUOUS_MODE, 100)

            while not self.Terminated:
                # return tuple : pktlen, data, timestamp
                res = self.p.next()
                if isinstance(res, types.TupleType):
                    self.packet_analyse(res)

            print 'sniffer : %d packets received, %d packets dropped, %d packets dropped by interface' % self.p.stats()

        except Exception as e:
            print "Sniffer : ", e
            raise


    def stop(self):
        self.Terminated = True

        print 'Sniffer : Pcap stop...'
        


    def packet_analyse(self, pkt):
        p = core.network_utils.packet_decode(pkt[0], pkt[1], pkt[2])
        
        core.network_utils.packet_show(p)

        print "---------------------"





if __name__ == "__main__":
    p = Sniffer()
    p.start()
    try:
        while 1:
            time.sleep(1)
    except KeyboardInterrupt:
        print "Stopping..."
    finally:
        p.stop()

