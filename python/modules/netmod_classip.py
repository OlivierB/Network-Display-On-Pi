#encoding: utf-8

"""
Client system monitoring

Use psutil

inherit from NetModule

@author: Olivier BLIN
"""


import time, psutil

import netmodule as netmod

from scapy.all import *

class MyMod(netmod.NetModule):
    def __init__(self, websocket=None):
        netmod.NetModule.__init__(self, websocket=websocket, updatetime=1, protocol='classip')
        

    def update(self):
        pass


    def pkt_handle(self, pkt):
    	p = Ether(pkt)
        if IP in p:
        	print p[IP].src, "->", p[IP].dst

    

