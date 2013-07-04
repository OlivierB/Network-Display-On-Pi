#encoding: utf-8

"""
Client system monitoring

inherit from NetModule

@author: Olivier BLIN
"""

# Python lib import
import time
import operator
import pcap

# Project file import
from netmodule import NetModule
from ndop.core.network import netdata
from ndop.core.network import netutils

MAX_IP_LIST_OUTSIDE = 1000
MAX_IP_LIST_SEND = 20
MAX_TIME_IP_LIST = 600


class NetModChild(NetModule):
    def __init__(self, *args, **kwargs):
        NetModule.__init__(self, updatetime=5, protocol='iplist', *args, **kwargs)

        # packet data
        self.lIPOut = dict()
        self.lIPOut_cleantime = time.time()

        self.lIP_tosend = self.get_ipout()
        self.lIP_next_start = 0

    def update(self):
        # Check if we need to update IP send list
        if self.lIP_next_start >= len(self.lIP_tosend):
            self.lIP_tosend = self.get_ipout()
            self.lIP_next_start = 0

        ip_nbr = len(self.lIP_tosend)
        ip_ns = self.lIP_next_start
        if ip_nbr > 0:
            val = dict()

            # val["iptop"] = self.get_ipout_top(maxip = 10)
                
            val['iplist'] = self.lIP_tosend[ip_ns:(ip_ns+MAX_IP_LIST_SEND)]
            self.lIP_next_start += MAX_IP_LIST_SEND

            # send data
            return val

    def pkt_handler(self, pkt):
        if pkt.Ether.is_type(netdata.ETHERTYPE_IPv4):
            src = pkt.Ether.payload.src
            # dst = pkt.Ether.payload.dst
            bsrc = netutils.ip_is_reserved(src)
            # bdst = netutils.ip_is_reserved(dst)
            if not bsrc:
                self.add_ip_list_outside(src, pkt.timestamp)

    def add_ip_list_outside(self, ip, timestamp):
        if len(self.lIPOut) < MAX_IP_LIST_OUTSIDE:
            if not ip in self.lIPOut.keys():
                self.lIPOut[ip] = dict()
                self.lIPOut[ip]["nbr"] = 1
                self.lIPOut[ip]["time"] = timestamp
            else:
                self.lIPOut[ip]["nbr"] += 1
                self.lIPOut[ip]["time"] = timestamp

            if (time.time() - self.lIPOut_cleantime) > MAX_TIME_IP_LIST:
                self.cleaniplist()
        else:
            self.cleaniplist()

    def cleaniplist(self):
        lastTime = self.lIPOut_cleantime
        r = sorted(self.lIPOut.values(), key=operator.itemgetter('nbr'))
        if len(r) > 0:
            limit = r[0]["nbr"]
        else:
            limit = 1
        t = time.time()
        map((lambda foo: self.__cleaniplist(foo, t, lastTime, limit)), self.lIPOut.keys())
        self.lIPOut_cleantime = time.time()

    def __cleaniplist(self, ip, t, lt, limit):
        diff = t - lt
        elem = self.lIPOut[ip]
        if not(((t - elem["time"]) < diff/2.0) or (elem["nbr"] > limit and (t - elem["time"]) < MAX_TIME_IP_LIST)):
            self.lIPOut.pop(ip)

    def get_ipout(self):
        return map(pcap.ntoa, self.lIPOut.keys())

    def get_ipout_top(self, maxip=20):
        l = list()
        nbip = 0
        sorted_l = sorted(self.lIPOut.iteritems(), key=operator.itemgetter(1), reverse=True)
        for e in sorted_l:
            l += [pcap.ntoa(e[0])]
            if not nbip < maxip:
                break
            nbip += 1
        return l
