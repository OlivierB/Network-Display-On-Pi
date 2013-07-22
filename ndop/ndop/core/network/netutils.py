# -*- coding: utf-8 -*-

"""
Network utils

@author: Olivier BLIN
"""

# Python lib import
import string
import socket
import struct
import logging
import pcap

# Project file import
from . import layer


def mac_to_string(data):
        return ':'.join('%02x' % ord(b) for b in data)


def ip_to_string(data):
    return socket.inet_ntoa(data)


def dumphex(s, sep="    "):
    bytes = map(lambda x: '%.2x' % x, map(ord, s))
    for i in xrange(0, len(bytes) / 16):
        print '%s%s' % (sep, string.join(bytes[i * 16:(i + 1) * 16], ' '))
    print '%s%s' % (sep, string.join(bytes[(i + 1) * 16:], ' '))


def ethertype_decode(v):
    # ''.join(struct.unpack('cc', v))
    return struct.unpack('cc', v)


def get_next_layer(underlayer, p_type, l_protocol, pktdata):

    if p_type in l_protocol.keys():
        prot = l_protocol[p_type]
        call = prot["callback"]
        if call is not None:
            try:
                return call(underlayer, pktdata, protocol=prot["protocol"])
            except layer.ProtocolMismatch as e:
                return None
            except layer.ProtocolError as e:
                logger = logging.getLogger()
                logger.debug("Layer %s (subprotocol : %s) - %s" % (
                             underlayer.protocol, prot["protocol"], e))
                return None
            except Exception as e:
                logger = logging.getLogger()
                logger.error("Layer %s (subprotocol : %s) - get_next_layer call : %r" % (
                             underlayer.protocol, prot["protocol"], e))
                logger.debug("Layer %s : error in call function" % underlayer.protocol, exc_info=True)
                return None
        else:
            return layer.Layer(underlayer, pktdata, protocol=prot["protocol"])
    else:
        return None


def ip_is_reserved(ip):

    dIPReserved = [
        (pcap.aton('0.0.0.0'), 8),        # Current network (only valid as source address)  RFC 5735
        (pcap.aton('10.0.0.0'), 8),       # Private network RFC 1918
        (pcap.aton('100.64.0.0'), 10),    # Shared Address Space    RFC 6598
        (pcap.aton('127.0.0.0'), 8),      # Loopback    RFC 5735
        (pcap.aton('169.254.0.0'), 16),   # Link-local  RFC 3927
        (pcap.aton('172.16.0.0'), 12),    # Private network RFC 1918
        (pcap.aton('192.0.0.0'), 24),     # IETF Protocol Assignments   RFC 5735
        (pcap.aton('192.0.2.0'), 24),     # TEST-NET-1, documentation and examples  RFC 5735
        (pcap.aton('192.88.99.0'), 24),   # IPv6 to IPv4 relay  RFC 3068
        (pcap.aton('192.168.0.0'), 16),   # Private network RFC 1918
        (pcap.aton('198.18.0.0'), 15),    # Network benchmark tests RFC 2544
        (pcap.aton('198.51.100.0'), 24),  # TEST-NET-2, documentation and examples  RFC 5737
        (pcap.aton('203.0.113.0'), 24),   # TEST-NET-3, documentation and examples  RFC 5737
        (pcap.aton('224.0.0.0'), 4),      # IP multicast (former Class D network)   RFC 5771
        (pcap.aton('240.0.0.0'), 4),      # Reserved (former Class E network)   RFC 1700
        (pcap.aton('255.255.255.255'), 32)  # Broadcast
    ]

    reserved = False
    for (net, m) in dIPReserved:
        mask = 0xffffffff >> (32 - m)
        if (ip & mask) == net:
            reserved = True
            break
    return reserved

def ip_is_reserved_net(ip):

    dIPReserved = [
        (pcap.aton('10.0.0.0'), 8),       # Private network RFC 1918
        (pcap.aton('100.64.0.0'), 10),    # Shared Address Space    RFC 6598
        (pcap.aton('127.0.0.0'), 8),      # Loopback    RFC 5735
        (pcap.aton('169.254.0.0'), 16),   # Link-local  RFC 3927
        (pcap.aton('172.16.0.0'), 12),    # Private network RFC 1918
        (pcap.aton('192.0.0.0'), 24),     # IETF Protocol Assignments   RFC 5735
        (pcap.aton('192.0.2.0'), 24),     # TEST-NET-1, documentation and examples  RFC 5735
        (pcap.aton('192.88.99.0'), 24),   # IPv6 to IPv4 relay  RFC 3068
        (pcap.aton('192.168.0.0'), 16),   # Private network RFC 1918
        (pcap.aton('198.18.0.0'), 15),    # Network benchmark tests RFC 2544
        (pcap.aton('198.51.100.0'), 24),  # TEST-NET-2, documentation and examples  RFC 5737
        (pcap.aton('203.0.113.0'), 24),   # TEST-NET-3, documentation and examples  RFC 5737
        (pcap.aton('224.0.0.0'), 4),      # IP multicast (former Class D network)   RFC 5771
        (pcap.aton('240.0.0.0'), 4),      # Reserved (former Class E network)   RFC 1700
    ]

    reserved = False
    for (net, m) in dIPReserved:
        mask = 0xffffffff >> (32 - m)
        if (ip & mask) == net:
            reserved = True
            break
    return reserved
