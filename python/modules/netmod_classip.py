#encoding: utf-8

"""
Client system monitoring

inherit from NetModule

@author: Olivier BLIN
"""


import time

import netmodule as netmod

import core.network.ethernet as ether

class NetModChild(netmod.NetModule):
    def __init__(self):
        netmod.NetModule.__init__(self, protocol='classip')

    def pkt_handler(self, pkt):
        if not pkt.Ether.is_type(ether.Ether_IPv4):
            print pkt


