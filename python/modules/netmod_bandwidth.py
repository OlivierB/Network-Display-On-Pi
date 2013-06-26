#encoding: utf-8

"""
Client system monitoring

Use psutil

inherit from NetModule

@author: Olivier BLIN
"""


import time, psutil, datetime

import netmodule as netmod

import core.network.utils as netutils
import core.network.netdata as netdata

class NetModChild(netmod.NetModule):
    def __init__(self):
        netmod.NetModule.__init__(self, updatetime=1, savetime=('m', 1), protocol='bandwidth')

        if psutil.__version__ < '0.7.0':
            print "Update psutil to 0.7.1"

        
        # packet data
        self.data = dict()
        self.data["pkt_nbr"] = 0
        self.data["net_load_loc"] = 0
        self.data["net_load_in"] = 0
        self.data["net_load_out"] = 0


        stat = self.sysState()
        
        # init
        self.oldValues = stat
        self.oldTotstats = stat


    def update(self):
        # System state update
        new = self.sysState()
        self.state = self.diffState(self.oldValues, new)
        self.oldValues = new

        # get data
        val = dict()
        val["tot_in_Ko"]    = self.state["net_speed_in"] / 1024
        val["tot_out_Ko"]   = self.state["net_speed_out"]  / 1024

        val["in_Ko"]    = self.state["net_load_in"] / 1024
        val["out_Ko"]   = self.state["net_load_out"]  / 1024

        val["loc_Ko"]   = self.state["net_load_loc"] / 1024
        val["Ko"]       = val["in_Ko"] + val["out_Ko"] + val["loc_Ko"]

        # send data
        return val


    def pkt_handler(self, pkt):
        self.data["pkt_nbr"] += 1

        if pkt.Ether.is_type(netdata.ETHERTYPE_IPv4):
            pkt_ipv4 = pkt.Ether.payload
            src = pkt_ipv4.src
            dst = pkt_ipv4.dst
            bsrc = netutils.ip_is_reserved(src)
            bdst = netutils.ip_is_reserved(dst)

            if bsrc and bdst:
                self.data["net_load_loc"] += pkt.pktlen
            elif not bsrc and bdst:
                self.data["net_load_in"] += pkt.pktlen
            elif bsrc and not bdst:
                self.data["net_load_out"] += pkt.pktlen


    def sysState(self):
        """
        Get system stats
        """

        val = dict()
        val["time"]     = time.time()
        val["net_sent"] = psutil.network_io_counters(pernic=False)[0]
        val["net_recv"] = psutil.network_io_counters(pernic=False)[1]
        val["net_load_loc"] = self.data["net_load_loc"]
        val["net_load_in"]  = self.data["net_load_in"]
        val["net_load_out"] = self.data["net_load_out"]

        return val

    def diffState(self, old, new):
        """
        System stats on diff time
        """
        val = dict()

        diff = new["time"] - old["time"]
        if diff <= 0:
            diff = 1

        # time in second.microsec
        val["time"]     = new["time"]
        val["dtime"]    = diff

        #  net data on device in o/sec
        val["net_speed_out"]    = (new["net_sent"] - old["net_sent"]) / diff
        val["net_speed_in"]     = (new["net_recv"] - old["net_recv"]) / diff
        # # net data by packet analysis
        val["net_load_loc"] = (new["net_load_loc"] - old["net_load_loc"]) / diff
        val["net_load_in"] = (new["net_load_in"] - old["net_load_in"]) / diff
        val["net_load_out"] = (new["net_load_out"] - old["net_load_out"]) / diff

        return val

    def totState(self, old, new):
        """
        System stats total
        """
        val = dict()

        # # net data by packet analysis
        val["net_load_loc"] = (new["net_load_loc"] - old["net_load_loc"])
        val["net_load_in"] = (new["net_load_in"] - old["net_load_in"])
        val["net_load_out"] = (new["net_load_out"] - old["net_load_out"])

        return val


    def save(self):
        req = "INSERT INTO bandwidth(global, local, incoming, outcoming) VALUES ("

        new = self.sysState()
        res = self.totState(self.oldTotstats, new)
        self.oldTotstats = new

        req += str(res["net_load_loc"]+res["net_load_in"]+res["net_load_out"]) + ","
        req += str(res["net_load_loc"]) + ","
        req += str(res["net_load_in"]) + ","
        req += str(res["net_load_out"])

        req += ")"
        return req