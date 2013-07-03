#encoding: utf-8

"""
Client system monitoring

Use psutil

inherit from NetModule

@author: Olivier BLIN
"""

# Python lib import
import time
import psutil

# Project file import
import netmodule as netmod


class NetModChild(netmod.NetModule):
    def __init__(self, *args, **kwargs):
        netmod.NetModule.__init__(self, updatetime=1, protocol='server_stat', *args, **kwargs)

        if psutil.__version__ < '0.7.0':
            print "Update psutil to 0.7.1"

        # packet data
        self.oldValues = self.sysState()

    def update(self):
        # System state update
        new = self.sysState()
        state = self.diffState(self.oldValues, new)
        self.oldValues = new

        # get data
        val = dict()
        val["mem_load"] = state["mem"]
        val["proc_load"] = state["cpu"]
        val["swap_load"] = state["swap"]

        # send data
        return val

    def sysState(self):
        """
        Get system stats
        """
        val = dict()
        val["time"] = time.time()
        val["mem"] = psutil.virtual_memory()[2]
        val["swap"] = psutil.swap_memory()[3]
        val["cpu"] = psutil.cpu_percent(interval=0)
        
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
        val["time"] = new["time"]
        val["dtime"] = diff

        # sys data in %
        val["mem"] = new["mem"]
        val["cpu"] = new["cpu"]
        val["swap"] = new["swap"]

        return val
