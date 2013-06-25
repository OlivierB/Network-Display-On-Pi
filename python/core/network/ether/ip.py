#encoding: utf-8

"""
Network implementation data

IP protocols class

@author: Olivier BLIN
"""

from .. import layer

import socket
import struct


class TCP(layer.Layer):
    def __init__(self, pktdata):
        layer.Layer.__init__(self, protocol="TCP")

        self.sport      = socket.ntohs(struct.unpack('H', pktdata[0:2])[0])
        self.dport      = socket.ntohs(struct.unpack('H', pktdata[2:4])[0])
        self.header_len = ord(pktdata[12]) >> 4

        self.payload = layer.Layer(pktdata[4*self.header_len:])


class UDP(layer.Layer):
    def __init__(self, pktdata):
        layer.Layer.__init__(self, protocol="UDP")

        self.sport      = socket.ntohs(struct.unpack('H', pktdata[0:2])[0])
        self.dport      = socket.ntohs(struct.unpack('H', pktdata[2:4])[0])
        self.len        = socket.ntohs(struct.unpack('H', pktdata[4:6])[0])

        self.payload = layer.Layer(pktdata[8:])
