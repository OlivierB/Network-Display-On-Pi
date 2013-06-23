#encoding: utf-8

"""
Client system monitoring

Use psutil

inherit from NetModule

@author: Olivier BLIN
"""


import time, psutil

import netmodule as netmod

class NetModChild(netmod.NetModule):
    def __init__(self):
        netmod.NetModule.__init__(self, updatetime=1, protocol='server_stat')

        if psutil.__version__ < '0.7.0':
            print "Update psutil to 0.7.1"

        # packet data
        self.oldValues = self.sysState()
        self.state = None

    def update(self):
        # System state update
        new = self.sysState()
        self.state = self.diffState(self.oldValues, new)
        self.oldValues = new

        # get data
        val = dict()
        val["mem_load"]     = self.state["mem"]
        val["proc_load"]    = self.state["cpu"]
        val["swap_load"]    = self.state["swap"]
        val["pkt_tot"], val["pkt_lost"] = 0, 0

        # send data
        return val


    def sysState(self):
        """
        Get system stats
        """
        val = dict()
        val["time"]     = time.time()
        val["mem"]      = psutil.virtual_memory()[2]
        val["swap"]     = psutil.swap_memory()[3]
        val["cpu"]      = psutil.cpu_percent(interval=0)
        val["sniff_stats"] = 0,0,0 #self.sniffer.stats() # nbp, plost with pcap, plost with device

        # # Disk data collect
        # val["io_read"]  = psutil.disk_io_counters(perdisk=False)[2]
        # val["io_write"] = psutil.disk_io_counters(perdisk=False)[3]

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

        # sys data in %
        val["mem"]      = new["mem"]
        val["cpu"]      = new["cpu"]
        val["swap"]     = new["swap"]

        # Packet stats
        ptot = (new["sniff_stats"][0] - old["sniff_stats"][0])
        plost = (new["sniff_stats"][1] - old["sniff_stats"][1])
        if ptot > 0:
            val["sniff_stats_ploss"] = plost/(ptot*1.0)*100
        else:
            val["sniff_stats_ploss"] = 0
        val["sniff_stats_ptot"] = new["sniff_stats"][0]

        # #  disk data in o/sec
        # val["disk_speed_read"]  = (new["io_read"] - old["io_read"]) / diff
        # val["disk_speed_write"] = (new["io_write"] - old["io_write"]) / diff

        return val



