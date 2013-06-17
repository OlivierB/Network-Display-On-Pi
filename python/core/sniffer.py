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
import operator

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
        self.nd = NetworkData()

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
                pkt = self.p.next()
                if isinstance(pkt, types.TupleType):
                    pktdec = core.network_utils.packet_decode(pkt[0], pkt[1], pkt[2])
                    self.nd.analyse(pktdec)


            # End
            a, b, c = self.p.stats()
            print 'sniffer : %d packets received, %d packets dropped, %d packets dropped by interface -' % self.p.stats(), b/(a*1.0+1)*100
            print self.nd.stats()

        except Exception as e:
            print "Sniffer : ", e
            raise

    def stop(self):
        self.Terminated = True

        print 'Sniffer : Pcap stop...'



class NetworkData(object):
    """
    Singleton class to collect network statistic
    """

    # Singleton creation
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(NetworkData, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    pkt_nbr = 0
    ip_list_outside = dict()
    # ip_list_inside = dict()


    def analyse(self, pkt):
        self.pkt_nbr += 1
        if pkt["Ethernet"]["EtherType"] == '\x08\x00':
            src = pkt["Ethernet"]["data"]["src"]
            dst = pkt["Ethernet"]["data"]["dst"]
            if not core.network_utils.ip_is_reserved(src):
                self.add_ip_list_outside(src)
            # else
            #     self.add_ip_list_inside(src)

    def add_ip_list_outside(self, ip):
        if len(self.ip_list_outside) < 500:
            if not ip in self.ip_list_outside.keys():
                self.ip_list_outside[ip] = 1
            else:
                self.ip_list_outside[ip] += 1
    
    def get_ip_list_outside(self):
        l = list()
        nbip = 0
        maxip = 10
        sorted_l = sorted(self.ip_list_outside.iteritems(), key=operator.itemgetter(1), reverse=True)
        for e in sorted_l:
            l += [pcap.ntoa(e[0])]
            if not nbip < maxip:
                break
            nbip += 1
        return l

    # def get_ip_list_inside(self):
    #     return self.ip_list_inside

    def stats(self,):
        return self.pkt_nbr




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

