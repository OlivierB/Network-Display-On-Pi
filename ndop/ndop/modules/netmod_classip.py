#encoding: utf-8

"""
Client system monitoring

inherit from NetModule

@author: Olivier BLIN
"""

# Project file import
from netmodule import NetModule


class NetModChild(NetModule):
    def __init__(self, *args, **kwargs):
        NetModule.__init__(self, protocol='classip', *args, **kwargs)

    def update(self):
        return None

    def pkt_handler(self, pkt):
        if pkt.is_protocol("Ethernet", "*"):
            print pkt.Ether
        pass

    def reset(self):
        """
        Clalled to reset module
        """
        pass

    def save(self):
        """
        Called to save module data in sql database every savetime
        
        return a list of sql request to save module content
            else return None

        """
        return None
