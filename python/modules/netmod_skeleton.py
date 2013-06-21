#encoding: utf-8

"""
Client system monitoring module

inherit from NetModule

@author: Olivier BLIN
"""

import netmodule as netmod

class MyMod(netmod.NetModule):
    def __init__(self, websocket):
        netmod.NetModule.__init__(self, websocket=websocket, updatetime=1, protocol='skeleton')

    def update(self):
        pass

    def pkt_handle(self, pkt):
    	pass