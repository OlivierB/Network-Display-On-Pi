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

PCAP_PROMISCUOUS_MODE   = 1

MAX_IP_LIST_OUTSIDE     = 1000
MAX_TIME_IP_LIST        = 120    # secondes

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

        except Exception as e:
            print "Sniffer : ", e
            raise

    def stop(self):
        self.Terminated = True

    def stats(self):
        self.p.stats()

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


    data = dict()

    data["pkt_nbr"] = 0
    data["net_load_loc"] = 0
    data["net_load_in"] = 0
    data["net_load_out"] = 0

    # ip list outside
    data["ipl_out"] = dict()
    data["ipl_out"]["tclean"] = time.time()
    data["ipl_out"]["ip"] = dict()
    data["ipl_in"] = dict() # ip list inside



    def analyse(self, pkt):
        self.data["pkt_nbr"] += 1
        if pkt["Ethernet"]["EtherType"] == '\x08\x00':
            src = pkt["Ethernet"]["data"]["src"]
            dst = pkt["Ethernet"]["data"]["dst"]
            bsrc = core.network_utils.ip_is_reserved(src)
            bdst = core.network_utils.ip_is_reserved(dst)

            if not core.network_utils.ip_is_reserved(src):
                self.add_ip_list_outside(src, pkt["pkt_timestamp"])
            # else:
            #     self.add_ip_list_inside(src)

            if bsrc and bdst:
                self.data["net_load_loc"] += pkt["pkt_len"]
            elif not bsrc and bdst:
                self.data["net_load_in"] += pkt["pkt_len"]
            elif bsrc and not bdst:
                self.data["net_load_out"] += pkt["pkt_len"]
            else:
                print "this packet is stupid"





    def add_ip_list_outside(self, ip, timestamp):
        if len(self.data["ipl_out"]["ip"]) < MAX_IP_LIST_OUTSIDE:
            if not ip in self.data["ipl_out"].keys():
                self.data["ipl_out"]["ip"][ip] = dict()
                self.data["ipl_out"]["ip"][ip]["nbr"] = 1
                self.data["ipl_out"]["ip"][ip]["time"] = timestamp
            else:
                self.data["ipl_out"]["ip"][ip]["nbr"] += 1
                self.data["ipl_out"]["ip"][ip]["time"] = timestamp

            if (time.time() - self.data["ipl_out"]["tclean"]) > MAX_TIME_IP_LIST:
                self.cleaniplist()

        else:
            self.cleaniplist()


    def cleaniplist(self):
        t = time.time()
        lastTime = self.data["ipl_out"]["tclean"]
        r = sorted(self.data["ipl_out"]["ip"].values(), key=operator.itemgetter('nbr'))
        if len(r) > 0:
            limit = r[0]["nbr"]
        else:
            limit = 1
        map((lambda foo: self.__cleaniplist(foo, t, lastTime, limit)), self.data["ipl_out"]["ip"].keys())
        self.data["ipl_out"]["tclean"] = time.time()
    

    def __cleaniplist(self, ip, t, lt, limit):
        diff = t - lt
        elem = self.data["ipl_out"]["ip"][ip]
        if not(((t - elem["time"]) < diff/2.0)\
            or (elem["nbr"] > limit and (t - elem["time"]) < MAX_TIME_IP_LIST)):
            self.data["ipl_out"]["ip"].pop(ip)
        

    def get_ip_list_outside(self):
        return map(pcap.ntoa, self.data["ipl_out"]["ip"].keys())

    def get_ip_list_outside_top(self, maxip = 20):
        l = list()
        nbip = 0
        sorted_l = sorted(self.data["ipl_out"]["ip"].iteritems(), key=operator.itemgetter(1), reverse=True)
        for e in sorted_l:
            l += [pcap.ntoa(e[0])]
            if not nbip < maxip:
                break
            nbip += 1
        return l

    # def get_ip_list_inside(self):
    #     return self.ip_list_inside

    def stats(self,):
        return self.data["pkt_nbr"]

    def get_netload_loc(self):
        return self.data["net_load_loc"] 
    def get_netload_in(self):
        return self.data["net_load_in"]
    def get_netload_out(self):
        return self.data["net_load_out"]

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

