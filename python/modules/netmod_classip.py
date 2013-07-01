#encoding: utf-8

"""
Client system monitoring

inherit from NetModule

@author: Olivier BLIN
"""

# Project file import
import netmodule as netmod

import os

class NetModChild(netmod.NetModule):
    def __init__(self):
        netmod.NetModule.__init__(self, protocol='classip')

    	self.nbp = 0

    def update(self):
        print "UP - %i" % os.getpid()
        return ('me', 5)

    def pkt_handler(self, pkt):
    	self.nbp +=1
    	# print pkt
        """
        Called by sniffer when a new packet arrive

        pkt is formated with Packet class
        """
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