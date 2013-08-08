# encoding: utf-8

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
from ndop.core.network import netutils


class NetModChild(NetModule):

    def __init__(self, *args, **kwargs):
        NetModule.__init__(self, updatetime=10, savetime=('m', 30), protocol='protocols', *args, **kwargs)

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
            res["ports"].append((netdata.PORTSLIST[k]["protocol"], diffval["ports"][k], k))

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

    def flow_handler(self, flow):
        protocol = flow.prot
        try:
            netdata.IPTYPE[protocol]
            if protocol in self.lIPProtocol:
                self.lIPProtocol[protocol] += 1
            else:
                self.lIPProtocol[protocol] = 1
                self.lIPList.append(protocol)
        except KeyError:
            pass



        if protocol == netdata.IPTYPE_TCP or protocol == netdata.IPTYPE_UDP:
            src = netutils.ip_reverse(flow.srcaddr_raw)
            dst = netutils.ip_reverse(flow.dstaddr_raw)

            bsrc = netutils.ip_is_reserved(src)
            bdst = netutils.ip_is_reserved(dst)

            port = -1
            if not bsrc:
                port = flow.srcport
            elif not bdst:
                port = flow.dstport
            else:
                try:
                    netdata.PORTSLIST[flow.srcport]
                    port = flow.srcport
                except KeyError:
                    try:
                        netdata.PORTSLIST[flow.dstport]
                        port = flow.dstport
                    except KeyError:
                        pass

            # List of IP protocols
            if port > 0:
                try:
                    netdata.PORTSLIST[port]
                    if port in self.lPortProtocol:
                        self.lPortProtocol[port] += 1
                    else:
                        self.lPortProtocol[port] = 1
                        self.lPortList.append(port)
                except KeyError:
                    pass



    def database_init(self, db_class):
        req = \
"""
CREATE TABLE IF NOT EXISTS `protocols_ether` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `protocol` varchar(60) NOT NULL,
  `number` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0 ;
"""
        db_class.execute(req)

        req = \
"""
CREATE TABLE IF NOT EXISTS `protocols_ip` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `protocol` varchar(60) NOT NULL,
  `number` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0 ;
"""
        db_class.execute(req)

        req = \
"""
CREATE TABLE IF NOT EXISTS `protocols_port` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `protocol` varchar(60) NOT NULL,
  `number` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0 ;
"""
        db_class.execute(req)

    def database_save(self, db_class):
        new = self.get_state()
        diffval = self.diff_states(self.save_oldstats, new)
        self.save_oldstats = new

        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.create_sql(db_class, diffval["ether"], netdata.ETHERTYPE, "protocols_ether", date, limit=5)

        self.create_sql(db_class, diffval["ip"], netdata.IPTYPE, "protocols_ip", date, limit=6)

        self.create_sql(db_class, diffval["ports"], netdata.PORTSLIST, "protocols_port", date, limit=10)


    def create_sql(self, db_class, data, l_prot_info, sql_table, sql_date, limit=5):
        l_couple = sorted(data.items(), key=operator.itemgetter(1), reverse=True)[:limit]
        for k, v in l_couple:
            if v > 0:
                req = "INSERT INTO " + sql_table + "(date, protocol, number) VALUES ("
                req += "\"" + sql_date + "\"" + ","
                req += "\"" + l_prot_info[k]["protocol"] + "\"" + ","
                req += str(v)
                req += ");"
            db_class.execute(req)

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
