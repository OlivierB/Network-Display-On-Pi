#encoding: utf-8

"""
Network utils

@author: Olivier BLIN
"""

# Python lib import
from . import ethernet as ether


class Packet():
    def __init__(self, pktlen=0, pktdata=None, timestamp=0):
        self.timestamp = timestamp
        self.pktlen = pktlen
        self.Ether = ether.Ethernet(pktdata)

    def __str__(self):
        tor = "< len : " + str(self.pktlen)
        tor += " - time : " + str(self.timestamp)
        tor += " " + self.Ether.__str__()
        tor += " >"
        return tor
