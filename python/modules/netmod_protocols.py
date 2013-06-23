#encoding: utf-8

"""
Client system monitoring

inherit from NetModule

@author: Olivier BLIN
"""


import time, operator

import netmodule as netmod

import core.network_callback

class NetModChild(netmod.NetModule):
    def __init__(self):
        netmod.NetModule.__init__(self, updatetime=1, protocol='protocols')

        # packet data
        self.lEtherProtocol = dict() # list protocol ethernet
        self.lIPProtocol = dict() # list protocol ip

    def update(self):
        # get data
        res = dict()
        val = dict()
        for k in self.lEtherProtocol.keys():
            val[core.network_callback.dEtherType[k]["protocol"]] = self.lEtherProtocol[k]
        res["ethernet"] = sorted(val.iteritems(), key=operator.itemgetter(1), reverse=True)

        val = dict()
        for k in self.lIPProtocol.keys():
            val[core.network_callback.dIPType[k]["protocol"]] = self.lIPProtocol[k]

        res["ip"] = sorted(val.iteritems(), key=operator.itemgetter(1), reverse=True)

        # send data
        return res


    def pkt_handler(self, pkt):
        # List of Ethernet protocols
        typ = pkt["Ethernet"]["EtherType"]
        if typ in core.network_callback.dEtherType.keys():
            if typ in self.lEtherProtocol:
                self.lEtherProtocol[typ] += 1
            else:
                self.lEtherProtocol[typ] = 1


        if typ == '\x08\x00':
            # List of IP protocols
            typ = pkt["Ethernet"]["data"]["data_protocol"]
            if typ in core.network_callback.dIPType.keys():
                if typ in self.lIPProtocol:
                    self.lIPProtocol[typ] += 1
                else:
                    self.lIPProtocol[typ] = 1
