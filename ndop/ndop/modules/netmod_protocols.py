# encoding: utf-8

"""
Client system monitoring

inherit from NetModule

@author: Olivier BLIN
"""

# Python lib import
import datetime
import operator
from time import time

# Project file import
from netmodule import NetModule
from ndop.core.network import netdata
from ndop.core.network import netutils


class NetModChild(NetModule):
    """
    List protocols used on 3 network's layers
    Ethernet statistics (EtherType [IPv4, IPv6, ARP, ...]) only works with the NDOP embed sniffer system
    """

    def __init__(self, *args, **kwargs):
        NetModule.__init__(self, updatetime=30, savecode=('m', 30), protocol='protocols', *args, **kwargs)

        # packet data
        self.lEtherProtocol = dict()  # list protocol ethernet
        self.lIPProtocol = dict()  # list protocol ip
        self.lPortProtocol = dict()  # list ports services

        self.lEtherList = list()
        self.lIPList = list()

        # stats
        val = self.get_state()
        self.save_oldstats = val
        self.update_oldstats = val
        
        # clear time
        self.max_live_port = 10
        self.add_conf_override("max_live_port")
        self.display_port_number = True
        self.add_conf_override("display_port_number")

        # Limit SVG
        self.bdd_max_ethertype = 5
        self.add_conf_override("bdd_max_ethertype")

        self.bdd_max_ipprotocol = 6
        self.add_conf_override("bdd_max_ipprotocol")

        self.bdd_max_port = 10
        self.add_conf_override("bdd_max_port")

        self.ignore_ipprotocol = list()
        self.add_conf_override("ignore_ipprotocol")

        self.ignore_port = list()
        self.add_conf_override("ignore_port")

        

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


        l_couple = sorted(diffval["ports"].items(), key=operator.itemgetter(1), reverse=True)[:self.max_live_port]
        res["ports"] = list()
        for k, v in l_couple:
            if v > 0:
                if self.display_port_number:
                    label = netdata.PORTSLIST[k]["protocol"] + " - " + str(k)
                else:
                    label = netdata.PORTSLIST[k]["protocol"]
                res["ports"].append((label, v))

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

            if type(self.ignore_ipprotocol) is list and typ in self.ignore_ipprotocol:
                typ = -1

            if typ in netdata.IPTYPE.keys():
                if typ in self.lIPProtocol:
                    self.lIPProtocol[typ] += 1
                else:
                    self.lIPProtocol[typ] = 1
                    self.lIPList.append(typ)

            if pkt.Ether.payload.is_type(netdata.IPTYPE_TCP) or pkt.Ether.payload.is_type(netdata.IPTYPE_UDP):
                # List of IP protocols
                port = pkt.Ether.payload.payload.type

                if type(self.ignore_port) is list and port in self.ignore_port:
                    port = -1

                try:
                    netdata.PORTSLIST[port]
                    try:
                        self.lPortProtocol[port] += 1
                    except KeyError:
                        self.lPortProtocol[port] = 1
                except KeyError:
                    pass

    def flow_handler(self, flow):
        protocol = flow.prot

        if type(self.ignore_ipprotocol) is list and protocol in self.ignore_ipprotocol:
            protocol = -1

        try:
            netdata.IPTYPE[protocol]
            if protocol in self.lIPProtocol:
                self.lIPProtocol[protocol] += flow.dPkts
            else:
                self.lIPProtocol[protocol] = flow.dPkts
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
            # Remove local ports (cannot determine good port)
            # else:
            #     try:
            #         netdata.PORTSLIST[flow.srcport]
            #         port = flow.srcport
            #     except KeyError:
            #         try:
            #             netdata.PORTSLIST[flow.dstport]
            #             port = flow.dstport
            #         except KeyError:
            #             pass

            # List of IP protocols
            if type(self.ignore_port) is list and port in self.ignore_port:
                port = -1

            if port > 0:
                try:
                    netdata.PORTSLIST[port]
                    try:
                        self.lPortProtocol[port] += flow.dPkts
                    except KeyError:
                        self.lPortProtocol[port] = flow.dPkts
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
  `port` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0 ;
"""
        db_class.execute(req)

    def database_save(self, db_class):
        new = self.get_state()
        diffval = self.diff_states(self.save_oldstats, new)
        self.save_oldstats = new

        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.create_sql(db_class, diffval["ether"], netdata.ETHERTYPE, "protocols_ether", date, limit=self.bdd_max_ethertype)

        self.create_sql(db_class, diffval["ip"], netdata.IPTYPE, "protocols_ip", date, limit=self.bdd_max_ipprotocol)

        self.create_sql_port(db_class, diffval["ports"], netdata.PORTSLIST, "protocols_port", date, limit=self.bdd_max_port)


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

    def create_sql_port(self, db_class, data, l_prot_info, sql_table, sql_date, limit=5):
        l_couple = sorted(data.items(), key=operator.itemgetter(1), reverse=True)[:limit]
        for k, v in l_couple:
            if v > 0:
                req = "INSERT INTO " + sql_table + "(date, protocol, number, port) VALUES ("
                req += "\"" + sql_date + "\"" + ","
                req += "\"" + l_prot_info[k]["protocol"] + "\"" + ","
                req += str(v) + ","
                req += str(k)
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
