#encoding: utf-8

"""
Client system monitoring

inherit from NetModule

@author: Olivier BLIN
"""

# Project file import
import netmodule as netmod


class NetModChild(netmod.NetModule):
    def __init__(self):
        netmod.NetModule.__init__(self, protocol='classip')

    def pkt_handler(self, pkt):
        print pkt
