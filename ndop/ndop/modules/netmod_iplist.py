# encoding: utf-8

"""
Client system monitoring

inherit from NetModule

Create a list of world contacted IP

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

MAX_IP_LIST_SEND = 20

class NetModChild(NetModule):

    def __init__(self, *args, **kwargs):
        NetModule.__init__(self, updatetime=5, protocol='iplist', *args, **kwargs)

        self.last_ip = set()

    def update(self):
        if len(self.last_ip) > 0:
            val = dict()
            val['iplist'] = map(pcap.ntoa, self.last_ip.copy())
            self.last_ip.clear()

            # send data
            return val

    def pkt_handler(self, pkt):
        if pkt.Ether.is_type(netdata.ETHERTYPE_IPv4):
            src = pkt.Ether.payload.src
            self.add_ip_list_outside(src)

    def flow_handler(self, flow):
        src = netutils.ip_reverse(flow.srcaddr_raw)
        self.add_ip_list_outside(src)

    def add_ip_list_outside(self, src):
        # use only src address to avoid broadcast address in dst

        bsrc = netutils.ip_is_reserved(src)

        if len(self.last_ip) <= MAX_IP_LIST_SEND and not bsrc:
            self.last_ip.add(src)
