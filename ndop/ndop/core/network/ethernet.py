# encoding: utf-8

"""
Network utils

@author: Olivier BLIN
"""

# Project file import
from . import layer
from ether import ip
from . import netutils


class Ethernet(layer.Layer):

    def decode(self, pktdata):
        self.src = pktdata[0:6]
        self.dst = pktdata[6:12]
        self.type = pktdata[12:14]

        # Ethernet protocol decode
        self.payload = netutils.get_next_layer(self, self.type, dEtherType, pktdata[14:])

    def __str__(self):
        tor = "[Ethernet " + self.payload.__str__() + "]"
        return tor

    def mac_to_string(self, data):
        return ':'.join('%02x' % ord(b) for b in data)


# EtherType list
dEtherType = {
    '\x08\x00': {'callback': ip.IPv4, 'protocol': 'IPv4', 'description': 'Internet Protocol version 4'},
    '\x08\x06': {'callback': None, 'protocol': 'ARP', 'description': 'Address Resolution Protocol'},
    '\x08\x42': {'callback': None, 'protocol': 'WoL', 'description': 'Wake on LAN'},
    '\x22\xF3': {'callback': None, 'protocol': 'IETF TRILL Protocol', 'description': 'Transparent Interconnection of Lots of Links - IETF Standard (Routing Bridges or TRILL Switches)'},
    '\x60\x03': {'callback': None, 'protocol': 'DECnet Phase IV', 'description': 'Network protocols - Digital Equipment Corporation'},
    '\x80\x35': {'callback': None, 'protocol': 'RARP', 'description': 'Reverse Address Resolution Protocol'},
    '\x80\x9B': {'callback': None, 'protocol': 'AppleTalk (Ethertalk)', 'description': 'Network protocols - Apple Inc.'},
    '\x80\xF3': {'callback': None, 'protocol': 'AARP', 'description': 'AppleTalk Address Resolution Protocol - Apple Inc.'},
    '\x81\x00': {'callback': None, 'protocol': 'VLAN-tag & SPB', 'description': 'VLAN-tagged frame (IEEE 802.1Q) & Shortest Path Bridging (IEEE 802.1aq)'},
    '\x81\x37': {'callback': None, 'protocol': 'IPX (alternatif)', 'description': 'Internetwork Packet Exchange'},
    '\x81\x38': {'callback': None, 'protocol': 'IPX', 'description': 'Internetwork Packet Exchange'},
    '\x82\x04': {'callback': None, 'protocol': 'QNX Qnet', 'description': 'network for a commercial Unix-like real-time operating system'},
    '\x86\xDD': {'callback': None, 'protocol': 'IPv6', 'description': 'Internet Protocol Version 6'},
    '\x88\x08': {'callback': None, 'protocol': 'Ethernet flow control', 'description': 'Priority-based flow control (IEEE 802.1Qbb)'},
    '\x88\x09': {'callback': None, 'protocol': 'Slow Protocols', 'description': 'Slow Protocols (IEEE 802.3)'},
    '\x88\x19': {'callback': None, 'protocol': 'CobraNet', 'description': 'Uncompressed, multi-channel, low-latency digital audio over a standard Ethernet network'},
    '\x88\x47': {'callback': None, 'protocol': 'MPLS unicast', 'description': 'Multiprotocol Label Switching'},
    '\x88\x48': {'callback': None, 'protocol': 'MPLS multicast', 'description': 'Multiprotocol Label Switching'},
    '\x88\x63': {'callback': None, 'protocol': 'PPPoE Discovery Stage', 'description': 'Point-to-Point Protocol over Ethernet'},
    '\x88\x64': {'callback': None, 'protocol': 'PPPoE Session Stage', 'description': 'Point-to-Point Protocol over Ethernet'},
    '\x88\x70': {'callback': None, 'protocol': 'Jumbo Frames', 'description': 'Ethernet frames with more than 1500 bytes of payload'},
    '\x88\x7B': {'callback': None, 'protocol': 'HomePlug 1.0 MME', 'description': 'Power line communications'},
    '\x88\x8E': {'callback': None, 'protocol': 'EAP over LAN', 'description': 'Extensible Authentication Protocol (IEEE 802.1X)'},
    '\x88\x92': {'callback': None, 'protocol': 'PROFINET Protocol', 'description': 'PROFINET uses standards such as TCP/IP and Ethernet'},
    '\x88\x9A': {'callback': None, 'protocol': 'HyperSCSI', 'description': 'SCSI over Ethernet'},
    '\x88\xA2': {'callback': None, 'protocol': 'AoE', 'description': 'ATA over Ethernet'},
    '\x88\xA4': {'callback': None, 'protocol': 'EtherCAT', 'description': 'Ethernet for Control Automation Technology'},
    '\x88\xA8': {'callback': None, 'protocol': 'PB & SPB', 'description': 'Provider Bridging (IEEE 802.1ad) & Shortest Path Bridging (IEEE 802.1aq)'},
    '\x88\xAB': {'callback': None, 'protocol': 'Ethernet Powerlink', 'description': 'Ethernet Powerlink expands Ethernet with a mixed polling and timeslicing mechanism'},
    '\x88\xCC': {'callback': None, 'protocol': 'LLDP', 'description': 'Link Layer Discovery Protocol'},
    '\x88\xCD': {'callback': None, 'protocol': 'SERCOS III', 'description': 'Communication between industrial controls, motion devices, and input/output devices '},
    '\x88\xE1': {'callback': None, 'protocol': 'HomePlug AV MME', 'description': 'Power line communications'},
    '\x88\xE3': {'callback': None, 'protocol': 'MRP', 'description': 'Media Redundancy Protocol (IEC 62439-2)'},
    '\x88\xE5': {'callback': None, 'protocol': 'MACsec', 'description': 'MAC security (IEEE 802.1AE)'},
    '\x88\xF7': {'callback': None, 'protocol': 'PTP', 'description': 'Precision Time Protocol (IEEE 1588)'},
    '\x89\x02': {'callback': None, 'protocol': 'CFM & OAM', 'description': 'Connectivity Fault Management (IEEE 802.1ag ) & Operations, Administration and Management (ITU-T)'},
    '\x89\x06': {'callback': None, 'protocol': 'FCoE', 'description': 'Fibre Channel over Ethernet'},
    '\x89\x14': {'callback': None, 'protocol': 'FCoE Initialization Protocol', 'description': 'Fibre Channel over Ethernet Initialization Protocol'},
    '\x89\x15': {'callback': None, 'protocol': 'RoCE', 'description': 'RDMA over Converged Ethernet'},
    '\x89\x2F': {'callback': None, 'protocol': 'HSR', 'description': 'High-availability Seamless Redundancy'},
    '\x90\x00': {'callback': None, 'protocol': 'ECTP', 'description': 'Ethernet Configuration Testing Protocol'},
    '\x91\x00': {'callback': None, 'protocol': 'Q-in-Q', 'description': 'Stacked VLANs - Multiple VLAN headers into a single frame (IEEE 802.1ad)'},
    '\xCA\xFE': {'callback': None, 'protocol': 'LLT', 'description': 'Veritas Low Latency Transport for Veritas Cluster Server'}
}
