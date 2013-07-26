# -*- coding: utf-8 -*-

"""
Network implementation data

x-ARP protocol

@author: Olivier BLIN
"""

# Python lib import
import socket
import struct

# Project file import
from .. import layer
from .. import netutils


class ARP(layer.Layer):

    def decode(self, pktdata):
        if len(pktdata) < 10:
            raise layer.ProtocolMismatch("Not enough data")

        self.hardware_type = socket.ntohs(struct.unpack('H', pktdata[0:2])[0])
        self.protocol_type = socket.ntohs(struct.unpack('H', pktdata[2:4])[0])
        self.hardware_len = (ord(pktdata[4]))
        self.protocol_len = (ord(pktdata[5]))
        # 1: request - 2: reply
        self.operation = socket.ntohs(struct.unpack('H', pktdata[6:8])[0])

        lh = self.hardware_len
        lp = self.protocol_len

        self.mac_src = 0
        self.ip_src = 0

        self.mac_dst = 0
        self.ip_dst = 0

        if lp == 4:
            self.mac_src = pktdata[8:8+lh]
            self.ip_src = struct.unpack('I', pktdata[8+lh:8+lh+lp])[0]

            self.mac_dst = pktdata[8+lh+lp:8+lh+lp+lh]
            self.ip_dst = struct.unpack('I', pktdata[8+lh+lp+lh:8+lh+lp+lh+lp])[0]
        elif lp == 16:
            self.mac_src = pktdata[8:8+lh]
            self.ip_src = struct.unpack('IIII', pktdata[8+lh:8+lh+lp])[0]

            self.mac_dst = pktdata[8+lh+lp:8+lh+lp+lh]
            self.ip_dst = struct.unpack('IIII', pktdata[8+lh+lp+lh:8+lh+lp+lh+lp])[0]

        # print self.operation, (netutils.mac_to_string(self.mac_src), 
        # netutils.ipi_to_string(self.ip_src), 
        # netutils.mac_to_string(self.mac_dst), 
        # netutils.ipi_to_string(self.ip_dst))
