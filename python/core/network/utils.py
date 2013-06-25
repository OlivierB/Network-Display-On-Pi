#encoding: utf-8

"""
Network utils

@author: Olivier BLIN
"""


import string
import socket
import struct
import types

import netdata


def mac_to_string(data):
        return ':'.join('%02x' % ord(b) for b in data)

def ip_to_string(data):
    return socket.inet_ntoa(data)

def dumphex(s, sep="    "):
    bytes = map(lambda x: '%.2x' % x, map(ord, s))
    for i in xrange(0,len(bytes)/16):
        print '%s%s' % (sep, string.join(bytes[i*16:(i+1)*16],' '))
    print '%s%s' % (sep, string.join(bytes[(i+1)*16:],' '))

def ethertype_decode(v):
    # ''.join(struct.unpack('cc', v))
    return struct.unpack('cc', v)

def ip_is_reserved(ip):
    reserved = False
    for (net, m) in netdata.IP_RESERVED:
        mask = 0xffffffff >> (32-m)
        if (ip & mask) == net:
            reserved = True
            break
    return reserved
