#encoding: utf-8

"""
Client system monitoring

Use psutil

inherit from NetModule

@author: Olivier BLIN
"""


import time, operator, pcap

import netmodule as netmod

import core.network_utils

LOCCOMM_MAX_IP  = 1000

class MyMod(netmod.NetModule):
    def __init__(self, websocket=None):
        netmod.NetModule.__init__(self, websocket=websocket, updatetime=1, protocol='local_communication')

        # packet data
        self.dIP_loccomm = dict()
        self.oldIPList = set()
        

    def update(self):
        # get data
        val = self.get_loc_comm()
 
        # send data
        self.send(val)

    def pkt_handle(self, pkt):
        if pkt["Ethernet"]["EtherType"] == '\x08\x00':

            src = pkt["Ethernet"]["data"]["src"]
            dst = pkt["Ethernet"]["data"]["dst"]
            bsrc = core.network_utils.ip_is_reserved(src)
            bdst = core.network_utils.ip_is_reserved(dst)

            if bsrc and bdst:
                self.add_loccomm(src, dst, pkt["pkt_len"])
            elif not bsrc and bdst:
                self.add_loccomm(-1, dst, pkt["pkt_len"])
            elif bsrc and not bdst:
                self.add_loccomm(src, -1, pkt["pkt_len"])
            else:
                print "This packet is stupid"


    def add_loccomm(self, src, dst, size):
        key = (src, dst)
        lk = self.dIP_loccomm.keys()
        if len(lk) < LOCCOMM_MAX_IP:
            if key in lk:
                val = self.dIP_loccomm[key]
                self.dIP_loccomm[key] = (val[0]+1, val[1]+size)
            else:
                self.dIP_loccomm[key] = (1, size)

    def get_loc_comm(self):
        val = dict()
        s_ip, val["communications"] = self.get_loccomm()
        val["remove_ip"] = list(self.oldIPList - s_ip)
        self.oldIPList = s_ip
        return val

    def get_loccomm(self):
        comm = self.dIP_loccomm
        self.dIP_loccomm = dict()

        l_ip = set()
        l_comm = list()
        for s, d in comm.keys():
            elem = comm[(s,d)]
            ss = self.ip_to_s(s)
            sd = self.ip_to_s(d)
            val = dict()
            val['ip_src'] = ss
            val['ip_dst'] = sd
            val['number'] = elem[0]
            val['size'] = elem[1]
            if s != -1:
                l_ip.add(ss)
            if d != -1:
                l_ip.add(sd)
            l_comm.append(val)
        return l_ip, l_comm

    def ip_to_s(self, ip):
        if ip == -1:
            return "internet"
        else:
            return pcap.ntoa(ip)