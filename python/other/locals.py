#encoding: utf-8

"""
@author: Olivier BLIN
"""

import pcap
from scapy.all import *
import types
import time
import copy

import core.network_callback
import core.network_utils
import core.packet

def fpcap():
    p = pcap.pcapObject()

    p.open_live("wlan0", 1600, 1, 750)

    return p

def sniff(p):
    pkt = None

    while pkt == None: # or pkt[0] < 300
        a = time.time()
        pkt = p.next()
        print "time : ", (time.time() - a)

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

    # res = core.network_utils.packet_decode(1200, pktd, 0)

    # pktscapy = Ether(pktd)
    # a = time.time()
    # for i in range(10000):
    #     r = pktscapy.copy()

    # print "time : ", (time.time() - a)

    # a = time.time()
    # for i in range(10000):
    #     r = Ether(pktd)

    # print "time : ", (time.time() - a)

    a = time.time()
    for i in range(1000000):
        res = core.network_utils.packet_decode(1200, pktd, 0)

    print "dic time : ", (time.time() - a)

    

    a = time.time()
    for i in range(1000000):
        pktdec = core.packet.Packet(1200, pktd, 0)

    print "class - time : ", (time.time() - a)

    # a = time.time()
    # for i in range(100000):
    #     r = ''.join(pktd)

    # print "time : ", (time.time() - a)



