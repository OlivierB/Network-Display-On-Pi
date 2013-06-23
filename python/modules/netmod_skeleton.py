#encoding: utf-8

"""
Skeleton
Module base

inherit from NetModule

@author: Olivier BLIN
"""

import time

import netmodule as netmod

class NetModChild(netmod.NetModule):
    def __init__(self):
        netmod.NetModule.__init__(self, updatetime=5, protocol='classip')


    def update(self):
        """
        Refresh method called every updatetime

        Return values to send to clients (websockets)
        automatically convert in json
        """
        return None

    def pkt_handler(self, pkt):
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
        Called to save module data

        heavy task

        """
        return None

