# encoding: utf-8

"""
Skeleton
Module base

inherit from NetModule

@author: Olivier BLIN
"""

# Project file import
from netmodule import NetModule
from ndop.core.network import netdata


class NetModChild(NetModule):
    """
    Retrieve domain name inside DNS packet
    """

    def __init__(self, *args, **kwargs):
        NetModule.__init__(self, updatetime=5, protocol='dns', *args, **kwargs)
        self.l_dns_name = list()

    def update(self):
        to_return = dict()
        to_return['list_dns_name'] = self.l_dns_name
        self.l_dns_name = list()
        return to_return

    def pkt_handler(self, pkt):
        if pkt.Ether.is_type(netdata.ETHERTYPE_IPv4):
            if pkt.Ether.payload.is_type(netdata.IPTYPE_UDP):
                if pkt.Ether.payload.payload.is_type(netdata.PORT_DNS):
                    if pkt.Ether.payload.payload.payload.dns_name != '':
                        self.l_dns_name.append(pkt.Ether.payload.payload.payload.dns_name)


    def database_save(self, db_class):
        """
        Called to save module data

        heavy task

        """
        return None
