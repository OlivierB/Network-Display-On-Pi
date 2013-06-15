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
        pkt["data_protocol"] = "?"
        pkt["data"] = pktdata
    
    return pkt

def packet_show(pkt):
    print "###[ %s ]###" % pkt["data_protocol"]
    recursive_show(pkt["data"], 0, '\t')

def recursive_show(pkt, lvl, sep):
    # Print all protocol information
    for key in pkt.keys():
        if not key in ["data", "data_protocol"]:
            print '%s%s=' % (sep*lvl, key), pkt[key]


    # Next protocol and data
    if isinstance(pkt["data"], types.DictType):
        if "data_protocol" in pkt.keys():
            print "%s###[ %s ]###" % (sep*(lvl+1) ,pkt["data_protocol"])
        recursive_show(pkt["data"], lvl+1, '\t')
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


# def decode_ip_packet(s):
#     d={}
#     d['version']=(ord(s[0]) & 0xf0) >> 4
#     d['header_len']=ord(s[0]) & 0x0f
#     d['tos']=ord(s[1])
#     d['total_len']=socket.ntohs(struct.unpack('H',s[2:4])[0])
#     d['id']=socket.ntohs(struct.unpack('H',s[4:6])[0])
#     d['flags']=(ord(s[6]) & 0xe0) >> 5
#     d['fragment_offset']=socket.ntohs(struct.unpack('H',s[6:8])[0] & 0x1f)
#     d['ttl']=ord(s[8])
#     d['protocol']=ord(s[9])
#     d['checksum']=socket.ntohs(struct.unpack('H',s[10:12])[0])
#     d['source_address']=pcap.ntoa(struct.unpack('i',s[12:16])[0])
#     d['destination_address']=pcap.ntoa(struct.unpack('i',s[16:20])[0])
#     if d['header_len']>5:
#         d['options']=s[20:4*(d['header_len']-5)]
#     else:
#         d['options']=None
#     d['data']=s[4*d['header_len']:]

#     return d


# def dumphex(s):
#     bytes = map(lambda x: '%.2x' % x, map(ord, s))
#     for i in xrange(0,len(bytes)/16):
#         print '    %s' % string.join(bytes[i*16:(i+1)*16],' ')
#     print '    %s' % string.join(bytes[(i+1)*16:],' ')
            
# def print_packet(pktlen, data, timestamp):
#     if not data:
#         return

#     if data[12:14]=='\x08\x00':
#         decoded=decode_ip_packet(data[14:])
#         print '\n%s.%f %s > %s' % ( time.strftime('%H:%M',
#                                     time.localtime(timestamp)),
#                                     timestamp % 60,
#                                     decoded['source_address'],
#                                     decoded['destination_address'])
#         for key in ['version', 'header_len', 'tos', 'total_len', 'id',
#                                 'flags', 'fragment_offset', 'ttl']:
#             print '  %s: %d' % (key, decoded[key])

#         prot = decoded['protocol']
#         if prot in core.network_callback.dIPType.keys():
#             prot = core.network_callback.dIPType[prot]["protocol"]

#         print '  protocol: %s' % prot
#         print '  header checksum: %d' % decoded['checksum']
#         print '  pkt len : ', pktlen
#         print '  data:'
#         dumphex(decoded['data'])
#         return



