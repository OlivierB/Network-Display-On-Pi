#encoding: utf-8

"""
@author: Olivier BLIN
"""

import pcap
# from scapy.all import *
import types
import time
import copy
import string

import core.network_callback
import core.network_utils
import core.network.packet as packet

def fpcap():
    p = pcap.pcapObject()

    p.open_live("eth1", 1600, 1, 750)

    return p

def sniff(p):
    pkt = None

    while pkt == None: # or pkt[0] < 300
        pkt = p.next()

    pktd = pkt[1]

    return pktd



# hexdump(pktd)

if __name__ == "__main__":
    p = fpcap()
    pktd = sniff(p)
    a = time.time()
    pkt = packet.Packet(pktdata=pktd)   
    print "time : ", (time.time() - a)
    print pkt.Ether









# class Data():
#     def __init__(self, data):
#         self.data = data
#         self.padding = 0

#     def get_i(self, i):
#         return self.data[i]

#     def add_padding(self, v):
#         self.padding += v

#     def __getitem__(self, index):
#         dec = self.padding + index
#         return self.data[dec]

#     def __setitem__(self, index, value):
#         pass

#     def __delitem__(self, index):
#         pass

#     def __getslice__(self, i, j):
#         a = max(0, i) + self.padding
#         b = max(0, j) + self.padding
#         return self.data[max(0, i):max(0, j):]

#     def __setslice__(self, i, j, seq):
#         pass

#     def __delslice__(self, i, j):
#         pass


