# encoding: utf-8

"""
Skeleton
Module base

inherit from NetModule

@author: Olivier BLIN
"""

# Project file import
from netmodule import NetModule


class NetModChild(NetModule):

    def __init__(self, *args, **kwargs):
        NetModule.__init__(self, updatetime=5, savetime=('m', 30), protocol='skeleton', *args, **kwargs)

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

    def database_init(self, db_class):
        """
        Clalled to init module database
        """
        pass

    def database_save(self, db_class):
        """
        Called to save module data in sql database every savetime

        return a list of sql request to save module content
            else return None

        """
        return None
