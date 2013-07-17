#encoding: utf-8

"""
@author: Olivier BLIN
"""

import pcap
# from scapy.all import *
import types
import time
import profile
import cProfile
import trace
import json
import base64
import sys


import core.network.packet as packet
import core.network.netdata as netdata

def fpcap():
    p = pcap.pcapObject()

    p.open_live("eth1", 1600, 1, 750)

    return p

def sniff(p):
    pkt = None

    while pkt == None: # or pkt[0] < 300
        a = time.time()
        pkt = p.next()
        print "time : ", (time.time() - a)

    pktd = pkt[1]

    return pktd

def put_file(name, nb=10):
    p = fpcap()
    cnt = 0
    lst = list()
    while cnt < nb:
        cnt += 1
        pktd = sniff(p)
        lst.append(base64.b64encode(pktd))
    f = open(name, 'w')
    f.write(json.dumps(lst))
    f.close()

def get_file(name):
    f = open(name, 'r')
    res = f.read()
    lst = list()
    res = json.loads(res)
    for r in res:
        lst.append(base64.b64decode(r))
    return lst

DEEP=6
def deeps(s, d, p):
    if d < DEEP:
        r = s[p+d:]
        deeps(s, d+1, p)

def deepsL(s, d, p):
    if d < DEEP:
        r = s[p:]
        deepsL(s[p:], d+1, p)
        


# hexdump(pktd)

def main():
    p = fpcap()
    pktd = sniff(p)



    ###########################################

    # pktdec = packet.Packet(1200, pktd, 0)

    # print pktdec

    ##########################################

    #  X Packet capture
    isFile = True
    try:
        with open('ListPackets'): pass
    except IOError:
        isFile = False

    if not isFile:
        put_file("ListPackets", nb=100)
        print "create"
    
    lpkt = get_file("ListPackets")


    ##########################################
    
    # #  X Packet capture
    # isFile = True
    # try:
    #     with open('ListPackets'): pass
    # except IOError:
    #     isFile = False

    # if not isFile:
    #     put_file("ListPackets", nb=1000)
    #     print "create"
    
    # fres = open('ResFile', 'a')
    # lpkt = get_file("ListPackets")
    # nbpkt = len(lpkt)
    # loop = 100

    # fres.write("Test with " + str(nbpkt)+" packets. Loop : "+str(loop)+" Time : ")
    # a = time.time()
    # for i in range(loop):
    #     for ppkt in lpkt:
    #         pktdec = packet.Packet(1200, ppkt, 0)

    # e = (time.time() - a)
    # print "File - time : ", e
    # fres.write(str(e)+"\n")

    ###########################################

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


    ###########################################

    # ttt = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # tt = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    
    # a = time.time()
    # for i in range(1000000):
    #     deeps(ttt, 0, 1)
    # print "dic time : ", (time.time() - a)

    # a = time.time()
    # for i in range(1000000):
    #     deepsL(ttt, 0, 1)
    # print "dic time : ", (time.time() - a)


    ###########################################


    # a = time.time()
    # for i in range(100000):
    #     res = core.network_utils.packet_decode(1200, pktd, 0)

    # print "dic time : ", (time.time() - a)

    
    fntdec = packet.Packet
    a = time.time()
    for i in xrange(1000):
        for p in lpkt:
            pktdec = fntdec(1200, p, 0)

    print "class - time : ", (time.time() - a)
    print pktdec

    # a = time.time()
    # for i in range(1000000):
    #     if res["Ethernet"]["EtherType"] == '\x08\x00':
    #         yy = res["Ethernet"]["data"]["src"]

    # print "dic time : ", (time.time() - a)

    

    # a = time.time()
    # for i in range(1000000):
    #     if pktdec.Ether.type == '\x08\x00':
    #         yy = pktdec.Ether.payload.src
        

    # print "class - time : ", (time.time() - a)

    ##########################################


    # a = time.time()
    # for i in range(100000):
    #     r = ''.join(pktd)

    # print "time : ", (time.time() - a)



    ##########################################

    # a = time.time()
    # for i in range(100000):
    #     if pktdec.Ether.is_type(netdata.ETHERTYPE_IPv4):
    #         if pktdec.Ether.payload.is_type(netdata.IPTYPE_TCP):
    #             if pktdec.Ether.payload.payload.is_type(netdata.TCPTYPE_HTTP):
    #                 pass
    # print "class - time : ", (time.time() - a)


    # a = time.time()
    # for i in range(100000):
    #     if pktdec.is_protocol("Ethernet", "IPv4", "TCP"):
    #         pass
    # print "class - time : ", (time.time() - a)


if __name__ == "__main__":
    # pr = profile.Profile()
    # for i in range(5):
    #     your_computed_bias = pr.calibrate(10000)

    # pr = profile.Profile(bias=your_computed_bias)


    # cProfile.run('main()', "profile_tmp4")
    main()


    
  # # create a Trace object, telling it what to ignore, and whether to
  # # do tracing or line-counting or both.
  # tracer = trace.Trace(ignoredirs=[sys.prefix, sys.exec_prefix,], trace=0, count=1)
  # # run the new command using the given tracer
  # tracer.run('main()')
  # # make a report, placing output in /tmp
  # r = tracer.results()
  # r.write_results(show_missing=True, coverdir="/tmp")