#encoding: utf-8

"""
Network utils

@author: Olivier BLIN
"""


import string
import socket
import struct
import types

import core.network_callback

def packet_decode(pktlen, pktdata, timestamp):
    pkt = dict()
    # packet information
    pkt["pkt_len"] = pktlen
    pkt["pkt_timestamp"] = timestamp

    # Ethernet frame decode
    pkt["data_protocol"] = "Ethernet"
    pkt["data"] = ethernet_decode(pktdata)

    return pkt

def ethernet_decode(pktdata):
    pkt = dict()
    pkt["mac_src"] = mac_to_string(pktdata[0:6])
    pkt["mac_dst"] = mac_to_string(pktdata[6:12])


    # Ethernet protocol decode
    typ = pktdata[12:14]
    pkt["EtherType"] = typ
    if typ in core.network_callback.dEtherType.keys()\
        and core.network_callback.dEtherType[typ]["callback"] != None:
        pkt["data_protocol"] = core.network_callback.dEtherType[typ]["protocol"]
        pkt["data"] = core.network_callback.dEtherType[typ]["callback"](pktdata[14:])
    else:
        pkt["data_protocol"] = "Unknown"
        pkt["data"] = pktdata
    
    return pkt

def packet_show(pkt):
    print "###[ %s ]###" % pkt["data_protocol"]
    recursive_show(pkt["data"], 0, '    ')

def recursive_show(pkt, lvl, sep):
    # Print all protocol information
    for key in pkt.keys():
        if not key in ["data", "data_protocol"]:
            print '%s%s=' % (sep*lvl, key), pkt[key]


    # Next protocol and data
    if isinstance(pkt["data"], types.DictType):
        if "data_protocol" in pkt.keys():
            print "%s###[ %s ]###" % (sep*(lvl+1) ,pkt["data_protocol"])
        recursive_show(pkt["data"], lvl+1, sep)
    else:
        
        if "data_protocol" in pkt.keys():
            print '%s%s=' % (sep*lvl, "data_protocol"), pkt["data_protocol"]
        print '%s%s=' % (sep*lvl, "data")
        dumphex(pkt["data"], sep*(lvl+1))

def mac_to_string(data):
    s = ""
    for i in range(6):
        tmp = "%x" % struct.unpack("B", data[i])
        while len(tmp) < 2:
            tmp = "0"+tmp
        s += tmp
        if i < 5:
            s += ":"
    return s

def dumphex(s, sep="    "):
    bytes = map(lambda x: '%.2x' % x, map(ord, s))
    for i in xrange(0,len(bytes)/16):
        print '%s%s' % (sep, string.join(bytes[i*16:(i+1)*16],' '))
    print '%s%s' % (sep, string.join(bytes[(i+1)*16:],' '))


