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
import datetime

# Project file import
from netmodule import NetModule
from ndop.core.sniffer import GetSniffer


class NetModChild(NetModule):
    def __init__(self, *args, **kwargs):
        NetModule.__init__(self, updatetime=1, savetime=('m', 30), protocol='packet_loss', *args, **kwargs)

        if psutil.__version__ < '0.7.0':
            print "Update psutil to 0.7.1"

        # packets stats
        self.sniff = GetSniffer()

        state = self.sysState()
        # init
        self.oldValues = state
        self.oldTotstats = state

    def update(self):
        # System state update
        new = self.sysState()
        state = self.diffState(self.oldValues, new)
        self.oldValues = new

        # send data
        return state

    def pkt_handler(self, pkt):
        pass

    def save(self):
        req = "INSERT INTO packet_loss(date, packet_received, packet_handled, dtime_s) VALUES ("

        new = self.sysState()
        res = self.totState(self.oldTotstats, new)
        self.oldTotstats = new

        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        req += "\"" + date + "\"" + ","
        req += str(res["pkt_all"]) + ","
        req += str(res["pkt_handle"]) + ","
        req += str(res["dtime"])

        req += ")"
        return req

        return None

    def sysState(self):
        """
        Get system stats
        """

        val = dict()

        val["time"] = time.time()

        res = self.sniff.get_stats()
        if res is not None:
            val["pkt_all"], val["pkt_drop"], val["pkt_devdrop"] = res
        else:
            val["pkt_all"], val["pkt_drop"], val["pkt_devdrop"] = (0,0,0)

        return val

    def diffState(self, old, new):
        """
        System stats on diff time
        """
        val = dict()

        diff = new["time"] - old["time"]
        if diff <= 0:
            diff = 1

        val["packet_received"] = new["pkt_all"] - old["pkt_all"]
        val["packet_dropped"] = new["pkt_drop"] - old["pkt_drop"]
        val["packet_devdrop"] = new["pkt_devdrop"] - old["pkt_devdrop"]
        val["packet_handled"] = val["packet_received"] - val["packet_dropped"]

        return val

    def totState(self, old, new):
        """
        System stats total
        """
        val = dict()

        diff = new["time"] - old["time"]
        if diff <= 0:
            diff = 1

        # time in second.microsec
        # val["time"] = new["time"]
        val["dtime"] = diff

        val["pkt_all"] = new["pkt_all"] - old["pkt_all"]

        # packer handle in statistic
        val["pkt_handle"] = val["pkt_all"] - (new["pkt_drop"] - old["pkt_drop"])

        return val
