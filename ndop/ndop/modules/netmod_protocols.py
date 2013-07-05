#encoding: utf-8

"""
Client system monitoring

inherit from NetModule

@author: Olivier BLIN
"""

# Python lib import
import datetime
import operator

# Project file import
from netmodule import NetModule
from ndop.core.network import netdata


class NetModChild(NetModule):
    def __init__(self, *args, **kwargs):
        NetModule.__init__(self, updatetime=30, savetime=('m', 30), protocol='protocols', *args, **kwargs)

        # packet data
        self.lEtherProtocol = dict()  # list protocol ethernet
        self.lIPProtocol = dict()  # list protocol ip
        self.lPortProtocol = dict()  # list ports services

        self.lEtherList = list()
        self.lIPList = list()
        self.lPortList = list()

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

        res["ports"] = list()
        for k in self.lPortList:
            res["ports"].append((netdata.PORTSLIST[k]["protocol"], diffval["ports"][k]))

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

            if pkt.Ether.payload.is_type(netdata.IPTYPE_TCP) or pkt.Ether.payload.is_type(netdata.IPTYPE_UDP):
                # List of IP protocols
                typ = pkt.Ether.payload.payload.type
                if typ in netdata.PORTSLIST.keys():
                    if typ in self.lPortProtocol:
                        self.lPortProtocol[typ] += 1
                    else:
                        self.lPortProtocol[typ] = 1
                        self.lPortList.append(typ)


    def save(self):
        lreq = list()

        new = self.get_state()
        diffval = self.diff_states(self.save_oldstats, new)
        self.save_oldstats = new

        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # for k in self.lEtherList:
        #     if diffval["ether"][k] > 0:
        #         req = "INSERT INTO protocols_ether(date, protocol, number) VALUES ("
        #         req += "\"" + date + "\"" + ","
        #         req += "\"" + netdata.ETHERTYPE[k]["protocol"] + "\"" + ","
        #         req += str(diffval["ether"][k])
        #         req += ");"
        #         lreq.append(req)

        # for k in self.lIPList:
        #     if diffval["ip"][k] > 0:
        #         req = "INSERT INTO protocols_ip(date, protocol, number) VALUES ("
        #         req += "\"" + date + "\"" + ","
        #         req += "\"" + netdata.IPTYPE[k]["protocol"] + "\"" + ","
        #         req += str(diffval["ip"][k])
        #         req += ");"
        #         lreq.append(req)

        lreq += self.create_sql(diffval["ether"], netdata.ETHERTYPE, "protocols_ether", date, limit=5)

        lreq += self.create_sql(diffval["ip"], netdata.IPTYPE, "protocols_ip", date, limit=6)

        lreq += self.create_sql(diffval["ports"], netdata.PORTSLIST, "protocols_port", date, limit=10)
        
        return lreq

    def create_sql(self, data, l_prot_info, sql_table, sql_date, limit=5):
        l_req = list()
        l_couple = sorted(data.items(), key=operator.itemgetter(1), reverse=True)[:limit]
        for k, v  in l_couple:
            if v > 0:
                req = "INSERT INTO "+ sql_table +"(date, protocol, number) VALUES ("
                req += "\"" + sql_date + "\"" + ","
                req += "\"" + l_prot_info[k]["protocol"] + "\"" + ","
                req += str(v)
                req += ");"
            l_req.append(req)
        return l_req


    def get_state(self):
        val = dict()

        val["ether"] = self.lEtherProtocol.copy()
        val["ip"] = self.lIPProtocol.copy()
        val["ports"] = self.lPortProtocol.copy()

        return val

    def diff_states(self, old, new):
        val = dict()

        keys = ["ether", "ip", "ports"]

        for key in keys:
            val[key] = dict()

            for k in new[key].keys():
                if k in old[key].keys():
                    val[key][k] = new[key][k] - old[key][k]
                else:
                    val[key][k] = new[key][k]

        return val
