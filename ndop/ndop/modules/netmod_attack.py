# encoding: utf-8

"""
Attack detection

inherit from NetModule

@author: Olivier BLIN
"""

# Project file import
from netmodule import NetModule
from ndop.core.network import netdata
from ndop.core.network import netutils

import pcap


class NetModChild(NetModule):

    def __init__(self, *args, **kwargs):
        NetModule.__init__(self, updatetime=1, savetime=('m', 30), protocol='attack', *args, **kwargs)

        self.lmac = dict()
        self.alert = set()

    def pkt_handler(self, pkt):
        if pkt.Ether.is_type(netdata.ETHERTYPE_IPv4):

            self.analyse(pkt)

    def update(self):
        val = dict()
        val["nb_"] = len(self.lmac)
        val["alert"] = sorted(self.alert)
        return val

    def database_init(self, db_class):
        pass

    def database_save(self, db_class):
        self.lmac = dict()
        self.alert = set()

    def analyse(self, pkt):
        self.analyse_mac(pkt)


    def analyse_mac(self, pkt):
        macs = pkt.Ether.src
        addrs = pkt.Ether.payload.src

        macd = pkt.Ether.dst
        addrd = pkt.Ether.payload.dst

        bsrc = netutils.ip_is_reserved(addrs)
        bdst = netutils.ip_is_reserved(addrd)

        # if macs == 0 or macd == 0 or macs == 0xffffffffffff or macd == 0xffffffffffff:
        #     return

        # if (addrs >> 24) == 255 or  (addrd >> 24) == 255:
        #     return

        if (not bsrc and not bdst) or addrs == addrd:
            self.alert.add("outside %s [%s] to %s [%s]" % (pcap.ntoa(addrs), netutils.mac_to_string(macs), pcap.ntoa(addrd), netutils.mac_to_string(macd)))  
        else:
            adds = self.add_mac(macs, addrs)
            addd = self.add_mac(macd, addrd)
            if not (adds and addd):
                if not adds:
                    self.alert.add("on source %s [%s] (to %s [%s])" % (pcap.ntoa(addrs), netutils.mac_to_string(macs), pcap.ntoa(addrd), netutils.mac_to_string(self.lmac[addrd])))
                else:
                    self.alert.add("on dest %s [%s] (from %s [%s])" % (pcap.ntoa(addrd), netutils.mac_to_string(macd), pcap.ntoa(addrs), netutils.mac_to_string(self.lmac[addrs])))

    def add_mac(self, mac, addr):
        try:
            smac = self.lmac[addr]
            if not smac == mac:
                return False
        except KeyError:
            self.lmac[addr] = mac
        return True

