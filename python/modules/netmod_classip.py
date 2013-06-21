#encoding: utf-8

"""
Client system monitoring

Use psutil

inherit from NetModule

@author: Olivier BLIN
"""


import time, psutil

import netmodule as netmod

import core.network_utils, core.network_callback

class MyMod(netmod.NetModule):
    def __init__(self, websocket=None):
        netmod.NetModule.__init__(self, websocket=websocket, updatetime=1, protocol='classip')
        

    def update(self):
        pass


    def pkt_handle(self, pkt):
        print "pkt : ", pkt

    

