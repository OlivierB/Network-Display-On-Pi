# -*- coding: utf-8 -*-

"""
Network implementation data

@author: Olivier BLIN
"""

########################################
# ETHERNET PROTOCOL
# File : core.network.ethernet.py
from . import ethernet

# List of Ethernet type
ETHERTYPE = ethernet.dEtherType

# Local variable
for typ in ethernet.dEtherType.keys():
    locals()["ETHERTYPE_"+ethernet.dEtherType[typ]["protocol"].replace(" ", "_")] = typ

########################################
# IP PROTOCOL
# File : core.network.ether.ip.py
from ether import ip

# List of IP type
IPTYPE = ip.dIPType
# Local variable
for typ in ip.dIPType.keys():
    locals()["IPTYPE_"+ip.dIPType[typ]["protocol"].replace(" ", "_")] = typ

########################################
# PORTS LIST
# File : core.network.ether.services.services.py
from ether.services import services

PORTSLIST = services.dPortsList
# Local variable
for typ in services.dPortsList.keys():
    locals()["PORT_"+services.dPortsList[typ]["protocol"].replace(" ", "_")] = typ
