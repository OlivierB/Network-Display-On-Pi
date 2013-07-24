# encoding: utf-8

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
from ndop.core.network import netutils
from ndop.core.network import netdata


class NetModChild(NetModule):

    def __init__(self, *args, **kwargs):
        NetModule.__init__(self, updatetime=1, savetime=('m', 30), protocol='bandwidth', *args, **kwargs)

        if psutil.__version__ < '0.7.0':
            print "Update psutil to 0.7.1"

        # packet data
        self.data = dict()
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
        state = self.diffState(self.oldValues, new)
        self.oldValues = new

        # send data
        return state

    def pkt_handler(self, pkt):

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

    def database_init(self, db_class):
        req = \
"""
CREATE TABLE IF NOT EXISTS `bandwidth` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `global` int(11) NOT NULL,
  `local` int(11) NOT NULL,
  `incoming` int(11) NOT NULL,
  `outcoming` int(11) NOT NULL,
  `dtime_s` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0 ;
"""
        db_class.execute(req)

    def database_save(self, db_class):
        req = "INSERT INTO bandwidth(date, global, local, incoming, outcoming, dtime_s) VALUES ("

        new = self.sysState()
        res = self.totState(self.oldTotstats, new)
        self.oldTotstats = new

        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        req += "\"" + date + "\"" + ","
        req += str(res["net_load_loc"] + res["net_load_in"] + res["net_load_out"]) + ","
        req += str(res["net_load_loc"]) + ","
        req += str(res["net_load_in"]) + ","
        req += str(res["net_load_out"]) + ","
        req += str(res["dtime"])

        req += ")"
        db_class.execute(req)

    def sysState(self):
        """
        Get system stats
        """
        val = dict()
        val["time"] = time.time()
        val["net_load_loc"] = self.data["net_load_loc"]
        val["net_load_in"] = self.data["net_load_in"]
        val["net_load_out"] = self.data["net_load_out"]

        res_net = psutil.network_io_counters(pernic=True)
        # bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout
        if self.dev in res_net.keys():
            val["net"] = res_net[self.dev]
            print val["net"]
        else:
            val["net"] = psutil.network_io_counters(pernic=False)

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

        # net data by packet analysis
        val["loc_Ko"] = (new["net_load_loc"] - old["net_load_loc"]) / diff / 1024
        val["in_Ko"] = (new["net_load_in"] - old["net_load_in"]) / diff / 1024
        val["out_Ko"] = (new["net_load_out"] - old["net_load_out"]) / diff / 1024
        val["Ko"] = val["in_Ko"] + val["out_Ko"] + val["loc_Ko"]

        #  net data on device in o/sec
        val["tot_out_Ko"] = (new["net"][0] - old["net"][0]) / diff / 1024
        val["tot_in_Ko"] = (new["net"][1] - old["net"][1]) / diff / 1024

        return val

    def totState(self, old, new):
        """
        System stats total
        """
        val = dict()
        diff = new["time"] - old["time"]
        val["dtime"] = diff

        # net data by packet analysis
        val["net_load_loc"] = (new["net_load_loc"] - old["net_load_loc"]) / 1024
        val["net_load_in"] = (new["net_load_in"] - old["net_load_in"]) / 1024
        val["net_load_out"] = (new["net_load_out"] - old["net_load_out"]) / 1024

        return val
