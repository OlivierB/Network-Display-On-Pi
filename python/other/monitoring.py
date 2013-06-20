#encoding: utf-8

"""
Client system monitoring

Use psutil

@author: Olivier BLIN
"""

import os
import psutil
import time
import sys
import threading
import base64

import core.sniffer



class Monitoring(threading.Thread):
    """
    System stats update
    Threading
    """

    def __init__(self, sniffer, inter=1):
        threading.Thread.__init__(self)

        self.sniffer = sniffer
        self.inter = inter
        self.Terminated = False
        self.state = None
        self.mutex = threading.Lock()


    def run(self):
        print "Monitoring : Server start..."

        # Check interval
        self.inter = round(self.inter)
        if self.inter < 1:
            self.inter = 1

        old = self.sysState()

        try:
            # work loop
            while not self.Terminated:
                # Start time
                begin = time.time()
                self.val = self.sysState()

                new = self.sysState()
                self.state = self.diffState(old, new)
                old = new

                # Sleep time
                diff = self.inter - (time.time() - begin)
                if diff < 0:
                    diff = 0

                time.sleep(diff)
        except:
            raise
            self.stop()


    def stop(self):
        self.Terminated = True
        print "Monitoring : Server stop..."


    def sysState(self):
        """
        Get the system stats
        """
        nd = core.sniffer.NetworkData()

        val = dict()

        val["time"]     = time.time()
        val["mem"]      = psutil.virtual_memory()[2]
        val["swap"]     = psutil.swap_memory()[3]
        val["io_read"]  = psutil.disk_io_counters(perdisk=False)[2]
        val["io_write"] = psutil.disk_io_counters(perdisk=False)[3]
        val["net_sent"] = psutil.network_io_counters(pernic=False)[0]
        val["net_recv"] = psutil.network_io_counters(pernic=False)[1]
        val["net_load_loc"] = nd.get_netload_loc()
        val["net_load_in"]  = nd.get_netload_in()
        val["net_load_out"] = nd.get_netload_out()
        val["cpu"]      = psutil.cpu_percent(interval=0.8)
        val["sniff_stats"] = self.sniffer.stats() # nbp, plost with pcap, plost with device

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

        #  net data on device in o/sec
        val["net_speed_out"]    = (new["net_sent"] - old["net_sent"]) / diff
        val["net_speed_in"]     = (new["net_recv"] - old["net_recv"]) / diff
        # net data by packet analysis
        val["net_load_loc"] = (new["net_load_loc"] - old["net_load_loc"]) / diff
        val["net_load_in"] = (new["net_load_in"] - old["net_load_in"]) / diff
        val["net_load_out"] = (new["net_load_out"] - old["net_load_out"]) / diff

        #  disk data in o/sec
        val["disk_speed_read"]  = (new["io_read"] - old["io_read"]) / diff
        val["disk_speed_write"] = (new["io_write"] - old["io_write"]) / diff

        
        # Packet stats
        ptot = (new["sniff_stats"][0] - old["sniff_stats"][0])
        plost = (new["sniff_stats"][1] - old["sniff_stats"][1])
        if ptot > 0:
            val["sniff_stats_ploss"] = plost/(ptot*1.0)*100
        else:
            val["sniff_stats_ploss"] = 0
        val["sniff_stats_ptot"] = new["sniff_stats"][0]

        return val





    def getState(self):
        return self.state

    def get_cpu(self):
        if self.state != None:
            return self.state["cpu"]
        else:
            return 0

    def get_mem(self):
        if self.state != None:
            return self.state["mem"]
        else:
            return 0

    def get_swap(self):
        if self.state != None:
            return self.state["swap"]
        else:
            return 0

    def get_net_out(self):
        if self.state != None:
            return self.state["net_speed_out"]
        else:
            return 0
            
    def get_net_in(self):
        if self.state != None:
            return self.state["net_speed_in"]
        else:
            return 0

    def get_netload_loc(self):
        if self.state != None:
            return self.state["net_load_loc"]
        else:
            return 0
            
    def get_netload_in(self):
        if self.state != None:
            return self.state["net_load_in"]
        else:
            return 0

    def get_netload_out(self):
        if self.state != None:
            return self.state["net_load_out"]
        else:
            return 0

    def get_pkt_stats(self):
        if self.state != None:
            return self.state["sniff_stats_ptot"], self.state["sniff_stats_ploss"]
        else:
            return 0, 0



if __name__ == "__main__":

    m = Monitoring()
    m.start()

    try:
        while 1:
            time.sleep(1)
            print m.getState()

    except KeyboardInterrupt:
        m.stop()


