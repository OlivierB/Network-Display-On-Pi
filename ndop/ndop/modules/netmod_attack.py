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

from time import time
from datetime import datetime
import pcap

MAC_MAX = 10000

class NetModChild(NetModule):

    def __init__(self, *args, **kwargs):
        NetModule.__init__(self, updatetime=1, savetime=('m', 30), protocol='attack', *args, **kwargs)

        self.alert_mode = False

        self.smac = set()
        self.mac_evol = Evolution()


        self.dmac = dict()
        self.alert = set()

        self.dip_info = dict()

    def pkt_handler(self, pkt):
        ether = pkt.Ether
        
        # MAC flooding
        if (self.mac_flooding(ether)):
            return

        if ether.is_type(netdata.ETHERTYPE_IPv4):
            ipv4 = ether.payload
            # IP spoofing
            self.ip_spoofing(ether)
                
            if ipv4.is_type(netdata.IPTYPE_UDP):
                # Port scan
                self.port_scaning(ether)
                # UDP flood
                self.udp_flooding(ether)

                if ipv4.payload.is_type(netdata.PORT_DNS):
                    # DNS spoofing
                    self.dns_spoofing(ether)

            elif ipv4.is_type(netdata.IPTYPE_TCP):
                # Port scan
                self.port_scaning(ether)
                # SYN flood
                self.syn_flooding(ether)
                
            elif ipv4.is_type(netdata.IPTYPE_ICMP):
                # ICMP flood
                self.icmp_spoofing(ether)

        elif ether.is_type(netdata.ETHERTYPE_ARP):
            # ARP spoofing
            self.arp_spoofing(ether)
        

    def update(self):
        val = dict()
        val["alert"] = sorted(self.alert)
        return val

    def database_init(self, db_class):
        pass

    def database_save(self, db_class):
        self.lmac = dict()
        self.alert = set()

    def get_date(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")



    def mac_flooding(self, pkt):
        # if pkt.src not in self.smac:
        #     self.smac.add(pkt.src)
        #     self.mac_evol.inc()
        # if self.mac_evol.get_evol() > 30:
        #     self.alert.add("MAC FLOOD + %i mac" % self.mac_evol.get_evol())
        #     return True
        # else:
        #     return False
        pass


    def port_scaning(self, pkt):

        pass

    def udp_flooding(self, pkt):
        pass

    def dns_spoofing(self, pkt):
        pass

    def icmp_spoofing(self, pkt):
        pass

    def arp_spoofing(self, pkt):
        pass

    def ip_spoofing(self, pkt):
        pass

    def syn_flooding(self, pkt):
        pass


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




class Evolution():
    def __init__(self, inter_sec=1):
        self.inter_sec = inter_sec
        self.number = 0
        self.last_time = time()
        self.last_evolution = 0

    def inc(self, nbr=1):
        self.number += nbr
        self.update()

    def update(self):
        diff = time() - self.last_time
        if diff > self.inter_sec:
            self.last_time = time()
            self.last_evolution = self.number / diff
            self.number = 0

    def get_evol(self):
        return self.last_evolution


