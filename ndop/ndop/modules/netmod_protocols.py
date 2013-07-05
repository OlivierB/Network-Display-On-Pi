#encoding: utf-8

"""
Client system monitoring

inherit from NetModule

@author: Olivier BLIN
"""

# Python lib import
import datetime

# Project file import
from netmodule import NetModule
from ndop.core.network import netdata


class NetModChild(NetModule):
    def __init__(self, *args, **kwargs):
        NetModule.__init__(self, updatetime=30, savetime=('m', 30), protocol='protocols', *args, **kwargs)

        # packet data
        self.lEtherProtocol = dict()  # list protocol ethernet
        self.lIPProtocol = dict()  # list protocol ip

        self.lEtherList = list()
        self.lIPList = list()

        # stats
        val = self.get_state()
        self.save_oldstats = val
        self.update_oldstats = val

    def update(self):
        new = self.get_state()
        diffval = self.diff_states(self.update_oldstats, new)
        self.update_oldstats = new

        # get data
        res = dict()
        res["ethernet"] = list()
        for k in self.lEtherList:
            res["ethernet"].append((netdata.ETHERTYPE[k]["protocol"], diffval["ether"][k]))

        res["ip"] = list()
        for k in self.lIPList:
            res["ip"].append((netdata.IPTYPE[k]["protocol"], diffval["ip"][k]))

        # send data
        return res

    def pkt_handler(self, pkt):
        # List of Ethernet protocols
        typ = pkt.Ether.type
        if typ in netdata.ETHERTYPE.keys():
            if typ in self.lEtherProtocol:
                self.lEtherProtocol[typ] += 1
            else:
                self.lEtherProtocol[typ] = 1
                self.lEtherList.append(typ)

        if pkt.Ether.is_type(netdata.ETHERTYPE_IPv4):
            # List of IP protocols
            typ = pkt.Ether.payload.type
            if typ in netdata.IPTYPE.keys():
                if typ in self.lIPProtocol:
                    self.lIPProtocol[typ] += 1
                else:
                    self.lIPProtocol[typ] = 1
                    self.lIPList.append(typ)

    def save(self):
        lreq = list()

        new = self.get_state()
        diffval = self.diff_states(self.save_oldstats, new)
        self.save_oldstats = new

        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for k in self.lEtherList:
            if diffval["ether"][k] > 0:
                req = "INSERT INTO protocols_ether(date, protocol, number) VALUES ("
                req += "\"" + date + "\"" + ","
                req += "\"" + netdata.ETHERTYPE[k]["protocol"] + "\"" + ","
                req += str(diffval["ether"][k])
                req += ");"
                lreq.append(req)

        for k in self.lIPList:
            if diffval["ip"][k] > 0:
                req = "INSERT INTO protocols_ip(date, protocol, number) VALUES ("
                req += "\"" + date + "\"" + ","
                req += "\"" + netdata.IPTYPE[k]["protocol"] + "\"" + ","
                req += str(diffval["ip"][k])
                req += ");"
                lreq.append(req)

        return lreq

    def get_state(self):
        val = dict()

        val["ether"] = self.lEtherProtocol.copy()
        val["ip"] = self.lIPProtocol.copy()

        return val

    def diff_states(self, old, new):
        val = dict()

        keys = ["ether", "ip"]

        for key in keys:
            val[key] = dict()

            for k in new[key].keys():
                if k in old[key].keys():
                    val[key][k] = new[key][k] - old[key][k]
                else:
                    val[key][k] = new[key][k]

        return val
