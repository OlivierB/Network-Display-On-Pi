#encoding: utf-8

"""
@author: Olivier BLIN
"""

import pcap
from scapy.all import *
import types
import time
import copy

import core.network_utils

def fpcap():
    p = pcap.pcapObject()

    p.open_live("wlan0", 1600, 1, 1000)

    return p

def sniff(p):
    pkt = p.next()

    while not(isinstance(pkt, types.TupleType)) and pkt[1] > 200:
        pkt = p.next()

    pktd = pkt[1]

    return pktd




# hexdump(pktd)

if __name__ == "__main__":
    p = fpcap()
    pktd = sniff(p)
    # nb = 0

    # t = time.time()
    # while time.time() - t < 10:
    #     pktd = sniff(p)
    #     nb += 1

    #     # for i in range(15):
    #     #     r = ''.join(pktd)

    # print nb

    # print p.stats()

    res = core.network_utils.packet_decode(1200, pktd, 0)

    # pktscapy = Ether(pktd)
    # a = time.time()
    # for i in range(10000):
    #     r = pktscapy.copy()

    # print "time : ", (time.time() - a)

    a = time.time()
    for i in range(10000):
        r = Ether(pktd)

    print "time : ", (time.time() - a)

    a = time.time()
    for i in range(10000):
        res = core.network_utils.packet_decode(1200, pktd, 0)

    print "time : ", (time.time() - a)

    a = time.time()
    for i in range(100000):
        r = ''.join(pktd)

    print "time : ", (time.time() - a)



