#encoding: utf-8

"""
Network implementation data

@author: Olivier BLIN
"""

########################################
# ETHERNET PROTOCOL
# File : core.network.ethernet.py
import ethernet

# List of Ethernet type
ETHERTYPE = ethernet.dEtherType

# Local variable
for typ in ethernet.dEtherType.keys():
    locals()["ETHERTYPE_"+ethernet.dEtherType[typ]["protocol"].replace(" ", "_")] = typ

########################################
# IP PROTOCOL
# File : core.network.ether.ip.py
import ether.ip

# List of reserved IP address on network
IP_RESERVED = ether.ip.dIPReserved

# List of IP type
IPTYPE = ether.ip.dIPType
# Local variable
for typ in ether.ip.dIPType.keys():
    locals()["IPTYPE_"+ether.ip.dIPType[typ]["protocol"].replace(" ", "_")] = typ

########################################
# IP PROTOCOL
# File : core.network.ether.ip.py
import ether.services.services as services

UDPTYPE = services.dUDPType
# Local variable
for typ in services.dUDPType.keys():
    locals()["UDPTYPE_"+services.dUDPType[typ]["protocol"].replace(" ", "_")] = typ
