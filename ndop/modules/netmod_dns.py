#encoding: utf-8

"""
Skeleton
Module base

inherit from NetModule

@author: Olivier BLIN
"""

# Project file import
import netmodule as netmod
import core.network.netdata as netdata


class NetModChild(netmod.NetModule):
    def __init__(self, *args, **kwargs):
        netmod.NetModule.__init__(self, updatetime=5, savetime=('m', 30), protocol='dns', *args, **kwargs)
        self.l_dns_name = list()

    def update(self):
        to_return = dict()
        to_return['list_dns_name'] = self.l_dns_name
        self.l_dns_name = list()
        return to_return

    def pkt_handler(self, pkt):
        if pkt.Ether.is_type(netdata.ETHERTYPE_IPv4):
            if pkt.Ether.payload.is_type(netdata.IPTYPE_UDP):
                if pkt.Ether.payload.payload.is_type(netdata.UDPTYPE_DNS):
                    if pkt.Ether.payload.payload.payload.dns_name != '':
                        self.l_dns_name.append(pkt.Ether.payload.payload.payload.dns_name)

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