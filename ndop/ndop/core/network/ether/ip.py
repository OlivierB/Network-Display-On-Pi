# -*- coding: utf-8 -*-

"""
Network implementation data

IP protocol

@author: Olivier BLIN
"""

# Python lib import
import socket
import struct

# Project file import
from .. import layer
from .. import netutils

import services.services as services


class IPv4(layer.Layer):

    def decode(self, pktdata):
        if len(pktdata) < 20:
            raise layer.ProtocolMismatch("Not enough data")

        self.header_len = ord(pktdata[0]) & 0x0f
        self.type = ord(pktdata[9])
        self.src = struct.unpack('I', pktdata[12:16])[0]
        self.dst = struct.unpack('I', pktdata[16:20])[0]

        # Optimization : ignore useless parameters
        # self.version = (ord(pktdata[0]) & 0xf0) >> 4
        # self.tos = ord(pktdata[1])
        # self.total_len = socket.ntohs(struct.unpack('H', pktdata[2:4])[0])
        # self.id = socket.ntohs(struct.unpack('H', pktdata[4:6])[0])
        # self.flags = (ord(pktdata[6]) & 0xe0) >> 5
        # self.fragment_offset = socket.ntohs(struct.unpack('H', pktdata[6:8])[0] & 0x1f)
        # self.ttl = ord(pktdata[8])
        # self.checksum = socket.ntohs(struct.unpack('H', pktdata[10:12])[0])

        # if self.header_len > 5:
        #     self.options = pktdata[20:4*(self.header_len-5)]
        # else:
        #     self.options = None

        # IP protocol decode
        self.payload = netutils.get_next_layer(self, self.type, dIPType, pktdata[4 * self.header_len:])


class TCP(layer.Layer):

    def decode(self, pktdata):
        if len(pktdata) < 12:
            raise layer.ProtocolMismatch("Not enough data")

        self.sport = socket.ntohs(struct.unpack('H', pktdata[0:2])[0])
        self.dport = socket.ntohs(struct.unpack('H', pktdata[2:4])[0])
        self.header_len = ord(pktdata[12]) >> 4

        self.type = select_port(self.sport, self.dport)

        self.payload = netutils.get_next_layer(self, self.type, services.dPortsList, pktdata[4 * self.header_len:])


class UDP(layer.Layer):

    def decode(self, pktdata):
        if len(pktdata) < 8:
            raise layer.ProtocolMismatch("Not enough data")

        self.sport = socket.ntohs(struct.unpack('H', pktdata[0:2])[0])
        self.dport = socket.ntohs(struct.unpack('H', pktdata[2:4])[0])
        self.len = socket.ntohs(struct.unpack('H', pktdata[4:6])[0])

        self.type = select_port(self.sport, self.dport)

        self.payload = netutils.get_next_layer(self, self.type, services.dPortsList, pktdata[8:])


def select_port(src, dst):
    """Select existant port"""
    list_ports = services.dPortsList.keys()
    if dst in list_ports:
        return dst
    elif src in list_ports:
        return src
    else:
        return -1


dIPType = {
#     0: {'callback': None, 'protocol': 'dCCP', 'description': 'IPv6 Hop-by-Hop Option'},
    1: {'callback': None, 'protocol': 'ICMP', 'description': 'Internet Control Message'},
    2: {'callback': None, 'protocol': 'IGMP', 'description': 'Internet Group Management'},
#     3: {'callback': None, 'protocol': 'GGP', 'description': 'Gateway-to-Gateway'},
    4: {'callback': None, 'protocol': 'IPv4', 'description': 'IPv4 encapsulation'},
#     5: {'callback': None, 'protocol': 'ST', 'description': 'Stream'},
    6: {'callback': TCP, 'protocol': 'TCP', 'description': 'Transmission Control'},
#     7: {'callback': None, 'protocol': 'CBT', 'description': 'CBT'},
#     8: {'callback': None, 'protocol': 'EGP', 'description': 'Exterior Gateway Protocol'},
#     9: {'callback': None, 'protocol': 'IGP', 'description': 'any private interior gateway (used by Cisco for their IGRP)'},
#     10: {'callback': None, 'protocol': 'BBN-RCC-MON', 'description': 'BBN RCC Monitoring'},
#     11: {'callback': None, 'protocol': 'NVP-II', 'description': 'Network Voice Protocol'},
#     12: {'callback': None, 'protocol': 'PUP', 'description': 'PUP'},
#     13: {'callback': None, 'protocol': 'ARGUS', 'description': 'ARGUS'},
#     14: {'callback': None, 'protocol': 'EMCON', 'description': 'EMCON'},
#     15: {'callback': None, 'protocol': 'XNET', 'description': 'Cross Net Debugger'},
#     16: {'callback': None, 'protocol': 'CHAOS', 'description': 'Chaos'},
    17: {'callback': UDP, 'protocol': 'UDP', 'description': 'User Datagram'},
#     18: {'callback': None, 'protocol': 'MUX', 'description': 'Multiplexing'},
#     19: {'callback': None, 'protocol': 'DCN-MEAS', 'description': 'DCN Measurement Subsystems'},
#     20: {'callback': None, 'protocol': 'HMP', 'description': 'Host Monitoring'},
#     21: {'callback': None, 'protocol': 'PRM', 'description': 'Packet Radio Measurement'},
#     22: {'callback': None, 'protocol': 'XNS-IDP', 'description': 'XEROX NS IDP'},
#     23: {'callback': None, 'protocol': 'TRUNK-1', 'description': 'Trunk-1'},
#     24: {'callback': None, 'protocol': 'TRUNK-2', 'description': 'Trunk-2'},
#     25: {'callback': None, 'protocol': 'LEAF-1', 'description': 'Leaf-1'},
#     26: {'callback': None, 'protocol': 'LEAF-2', 'description': 'Leaf-2'},
#     27: {'callback': None, 'protocol': 'RDP', 'description': 'Reliable Data Protocol'},
#     28: {'callback': None, 'protocol': 'IRTP', 'description': 'Internet Reliable Transaction'},
#     29: {'callback': None, 'protocol': 'ISO-TP4', 'description': 'ISO Transport Protocol Class 4'},
#     30: {'callback': None, 'protocol': 'NETBLT', 'description': 'Bulk Data Transfer Protocol'},
#     31: {'callback': None, 'protocol': 'MFE-NSP', 'description': 'MFE Network Services Protocol'},
#     32: {'callback': None, 'protocol': 'MERIT-INP', 'description': 'MERIT Internodal Protocol'},
#     33: {'callback': None, 'protocol': 'DCCP', 'description': 'Datagram Congestion Control Protocol'},
#     34: {'callback': None, 'protocol': '3PC', 'description': 'Third Party Connect Protocol'},
#     35: {'callback': None, 'protocol': 'IDPR', 'description': 'Inter-Domain Policy Routing Protocol'},
#     36: {'callback': None, 'protocol': 'XTP', 'description': 'XTP'},
#     37: {'callback': None, 'protocol': 'DDP', 'description': 'Datagram Delivery Protocol'},
#     38: {'callback': None, 'protocol': 'IDPR-CMTP', 'description': 'IDPR Control Message Transport Proto'},
#     39: {'callback': None, 'protocol': 'TP++', 'description': 'TP++ Transport Protocol'},
#     40: {'callback': None, 'protocol': 'IL', 'description': 'IL Transport Protocol'},
    41: {'callback': None, 'protocol': 'IPv6', 'description': 'IPv6 encapsulation'},
#     42: {'callback': None, 'protocol': 'SDRP', 'description': 'Source Demand Routing Protocol'},
#     43: {'callback': None, 'protocol': 'IPv6-Route', 'description': 'Routing Header for IPv6'},
#     44: {'callback': None, 'protocol': 'IPv6-Frag', 'description': 'Fragment Header for IPv6'},
#     45: {'callback': None, 'protocol': 'IDRP', 'description': 'Inter-Domain Routing Protocol'},
#     46: {'callback': None, 'protocol': 'RSVP', 'description': 'Reservation Protocol'},
    47: {'callback': None, 'protocol': 'GRE', 'description': 'Generic Routing Encapsulation'},
#     48: {'callback': None, 'protocol': 'DSR', 'description': 'Dynamic Source Routing Protocol'},
#     49: {'callback': None, 'protocol': 'BNA', 'description': 'BNA'},
#     50: {'callback': None, 'protocol': 'ESP', 'description': 'Encap Security Payload'},
#     51: {'callback': None, 'protocol': 'AH', 'description': 'Authentication Header'},
#     52: {'callback': None, 'protocol': 'I-NLSP', 'description': 'Integrated Net Layer Security TUBA'},
#     53: {'callback': None, 'protocol': 'SWIPE', 'description': 'IP with Encryption'},
#     54: {'callback': None, 'protocol': 'NARP', 'description': 'NBMA Address Resolution Protocol'},
#     55: {'callback': None, 'protocol': 'MOBILE', 'description': 'IP Mobility'},
#     56: {'callback': None, 'protocol': 'TLSP', 'description': 'Transport Layer Security Protocol using Kryptonet key management'},
#     57: {'callback': None, 'protocol': 'SKIP', 'description': 'SKIP'},
    58: {'callback': None, 'protocol': 'IPv6-ICMP', 'description': 'ICMP for IPv6'},
#     59: {'callback': None, 'protocol': 'IPv6-NoNxt', 'description': 'No Next Header for IPv6'},
#     60: {'callback': None, 'protocol': 'IPv6-Opts', 'description': 'Destination Options for IPv6'},
#     61: {'callback': None, 'protocol': 'None', 'description': 'any host internal protocol'},
#     62: {'callback': None, 'protocol': 'CFTP', 'description': 'CFTP'},
#     63: {'callback': None, 'protocol': 'None', 'description': 'any local network'},
#     64: {'callback': None, 'protocol': 'SAT-EXPAK', 'description': 'SATNET and Backroom EXPAK'},
#     65: {'callback': None, 'protocol': 'KRYPTOLAN', 'description': 'Kryptolan'},
#     66: {'callback': None, 'protocol': 'RVD', 'description': 'MIT Remote Virtual Disk Protocol'},
#     67: {'callback': None, 'protocol': 'IPPC', 'description': 'Internet Pluribus Packet Core'},
#     68: {'callback': None, 'protocol': 'None', 'description': 'any distributed file system'},
#     69: {'callback': None, 'protocol': 'SAT-MON', 'description': 'SATNET Monitoring'},
#     70: {'callback': None, 'protocol': 'VISA', 'description': 'VISA Protocol'},
#     71: {'callback': None, 'protocol': 'IPCV', 'description': 'Internet Packet Core Utility'},
#     72: {'callback': None, 'protocol': 'CPNX', 'description': 'Computer Protocol Network Executive'},
#     73: {'callback': None, 'protocol': 'CPHB', 'description': 'Computer Protocol Heart Beat'},
#     74: {'callback': None, 'protocol': 'WSN', 'description': 'Wang Span Network'},
#     75: {'callback': None, 'protocol': 'PVP', 'description': 'Packet Video Protocol'},
#     76: {'callback': None, 'protocol': 'BR-SAT-MON', 'description': 'Backroom SATNET Monitoring'},
#     77: {'callback': None, 'protocol': 'SUN-ND', 'description': 'SUN ND PROTOCOL-Temporary'},
#     78: {'callback': None, 'protocol': 'WB-MON', 'description': 'WIDEBAND Monitoring'},
#     79: {'callback': None, 'protocol': 'WB-EXPAK', 'description': 'WIDEBAND EXPAK'},
#     80: {'callback': None, 'protocol': 'ISO-IP', 'description': 'ISO Internet Protocol'},
#     81: {'callback': None, 'protocol': 'VMTP', 'description': 'VMTP'},
#     82: {'callback': None, 'protocol': 'SECURE-VMTP', 'description': 'SECURE-VMTP'},
#     83: {'callback': None, 'protocol': 'VINES', 'description': 'VINES'},
#     84: {'callback': None, 'protocol': 'TTP', 'description': 'TTP'},
#     84: {'callback': None, 'protocol': 'IPTM', 'description': 'Protocol Internet Protocol Traffic Manager'},
#     85: {'callback': None, 'protocol': 'NSFNET-IGP', 'description': 'NSFNET-IGP'},
#     86: {'callback': None, 'protocol': 'DGP', 'description': 'Dissimilar Gateway Protocol'},
#     87: {'callback': None, 'protocol': 'TCF', 'description': 'TCF'},
#     88: {'callback': None, 'protocol': 'EIGRP', 'description': 'EIGRP'},
#     89: {'callback': None, 'protocol': 'OSPFIGP', 'description': 'OSPFIGP'},
#     90: {'callback': None, 'protocol': 'Sprite-RPC', 'description': 'Sprite RPC Protocol'},
#     91: {'callback': None, 'protocol': 'LARP', 'description': 'Locus Address Resolution Protocol'},
#     92: {'callback': None, 'protocol': 'MTP', 'description': 'Multicast Transport Protocol'},
#     93: {'callback': None, 'protocol': 'AX.25', 'description': 'AX.25 Frames'},
#     94: {'callback': None, 'protocol': 'IPIP', 'description': 'IP-within-IP Encapsulation Protocol'},
#     95: {'callback': None, 'protocol': 'MICP', 'description': 'Mobile Internetworking Control Pro.'},
#     96: {'callback': None, 'protocol': 'SCC-SP', 'description': 'Semaphore Communications Sec. Pro.'},
#     97: {'callback': None, 'protocol': 'ETHERIP', 'description': 'Ethernet-within-IP Encapsulation'},
#     98: {'callback': None, 'protocol': 'ENCAP', 'description': 'Encapsulation Header'},
#     99: {'callback': None, 'protocol': 'None', 'description': 'any private encryption scheme'},
#     100: {'callback': None, 'protocol': 'GMTP', 'description': 'GMTP'},
#     101: {'callback': None, 'protocol': 'IFMP', 'description': 'Ipsilon Flow Management Protocol'},
#     102: {'callback': None, 'protocol': 'PNNI', 'description': 'PNNI over IP'},
#     103: {'callback': None, 'protocol': 'PIM', 'description': 'Protocol Independent Multicast'},
#     104: {'callback': None, 'protocol': 'ARIS', 'description': 'ARIS'},
#     105: {'callback': None, 'protocol': 'SCPS', 'description': 'SCPS'},
#     106: {'callback': None, 'protocol': 'QNX', 'description': 'QNX'},
#     107: {'callback': None, 'protocol': 'A/N', 'description': 'Active Networks'},
#     108: {'callback': None, 'protocol': 'IPComp', 'description': 'IP Payload Compression Protocol'},
#     109: {'callback': None, 'protocol': 'SNP', 'description': 'Sitara Networks Protocol'},
#     110: {'callback': None, 'protocol': 'Compaq-Peer', 'description': 'Compaq Peer Protocol'},
#     111: {'callback': None, 'protocol': 'IPX-in-IP', 'description': 'IPX in IP'},
#     112: {'callback': None, 'protocol': 'VRRP', 'description': 'Virtual Router Redundancy Protocol'},
#     113: {'callback': None, 'protocol': 'PGM', 'description': 'PGM Reliable Transport Protocol'},
#     114: {'callback': None, 'protocol': 'None', 'description': 'any 0-hop protocol'},
#     115: {'callback': None, 'protocol': 'L2TP', 'description': 'Layer Two Tunneling Protocol'},
#     116: {'callback': None, 'protocol': 'DDX', 'description': 'D-II Data Exchange (DDX)'},
#     117: {'callback': None, 'protocol': 'IATP', 'description': 'Interactive Agent Transfer Protocol'},
#     118: {'callback': None, 'protocol': 'STP', 'description': 'Schedule Transfer Protocol'},
#     119: {'callback': None, 'protocol': 'SRP', 'description': 'SpectraLink Radio Protocol'},
#     120: {'callback': None, 'protocol': 'UTI', 'description': 'UTI'},
#     121: {'callback': None, 'protocol': 'SMP', 'description': 'Simple Message Protocol'},
#     122: {'callback': None, 'protocol': 'SM', 'description': 'SM'},
#     123: {'callback': None, 'protocol': 'PTP', 'description': 'Performance Transparency Protocol'},
#     124: {'callback': None, 'protocol': 'ISIS over IPv4', 'description': ''},
#     125: {'callback': None, 'protocol': 'FIRE', 'description': ''},
#     126: {'callback': None, 'protocol': 'CRTP', 'description': 'Combat Radio Transport Protocol'},
#     127: {'callback': None, 'protocol': 'CRUDP', 'description': 'Combat Radio User Datagram'},
#     128: {'callback': None, 'protocol': 'SSCOPMCE', 'description': ''},
#     129: {'callback': None, 'protocol': 'IPLT', 'description': ''},
#     130: {'callback': None, 'protocol': 'SPS', 'description': 'Secure Packet Shield'},
#     131: {'callback': None, 'protocol': 'PIPE', 'description': 'Private IP Encapsulation within IP'},
#     132: {'callback': None, 'protocol': 'SCTP', 'description': 'Stream Control Transmission Protocol'},
#     133: {'callback': None, 'protocol': 'FC', 'description': 'Fibre Channel'},
#     134: {'callback': None, 'protocol': 'RSVP-E2E-IGNORE', 'description': ''},
#     135: {'callback': None, 'protocol': 'Mobility Header', 'description': ''},
#     136: {'callback': None, 'protocol': 'UDPLite', 'description': ''},
#     137: {'callback': None, 'protocol': 'MPLS-in-IP', 'description': ''},
#     138: {'callback': None, 'protocol': 'manet', 'description': 'MANET Protocols'},
#     139: {'callback': None, 'protocol': 'HIP', 'description': 'Host Identity Protocol'},
#     140: {'callback': None, 'protocol': 'Shim6', 'description': 'Shim6 Protocol'},
#     141: {'callback': None, 'protocol': 'WESP', 'description': 'Wrapped Encapsulating Security Payload'},
#     142: {'callback': None, 'protocol': 'ROHC', 'description': 'Robust Header Compression'}
}
