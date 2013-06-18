#encoding: utf-8

"""
System Information collector

Optimization of websocket send

@author: Olivier BLIN
"""

import time

import core.sniffer, core.wsserver, core.monitoring

WSSUBPROT_SYSDATA       = 'server_stat'
WSSUBPROT_BANDWIDTH     = 'bandwidth'
WSSUBPROT_IPLIST        = 'iplist'
WSSUBPROT_ALERT         = 'alert'
WSSUBPROT_PROTOCOLS     = 'protocols'

MAX_IP_LIST_SEND        = 20

# UPDATE TIME
TIME_UPDATE_IPTOP       = 60
TIME_UPDATE_PROTOCOLS   = 5


class Update():
    def __init__(self, monnitor, sniffer):
        self.m = monnitor
        self.sniff = sniffer
        self.datanet = core.sniffer.NetworkData()
        self.cl = core.wsserver.ClientsList()

        # values save
        self.sysdata    = self.__get_sysdata()
        self.bandwidth  = self.__get_bandwidth()
        self.iplist     = self.__get_iplist()

        # time list for update
        self.time = dict()
        self.time["timeiptop"]  = 0
        self.time["protocols"]  = 0

    #  Global update
    def update(self):
        self.__update_sysdata()
        self.__update_bandwidth()
        self.__update_iplist()
        self.__update_alert()
        self.__update_protocols()

    # System data managment
    def __update_sysdata(self):
        val = self.__get_sysdata()
        self.cl.send(WSSUBPROT_SYSDATA, val)
        self.sysdata = val

    def __get_sysdata(self):
        val = dict()
        val["mem_load"]     = self.m.get_mem()
        val["proc_load"]    = self.m.get_cpu()
        val["swap_load"]    = self.m.get_swap()
        val["pkt_tot"], val["pkt_lost"] = self.m.get_pkt_stats()
        return val


    # Bandwidth information
    def __update_bandwidth(self):
        val = self.__get_bandwidth()
        if self.__diff_bandwidth(val):
            self.cl.send(WSSUBPROT_BANDWIDTH, val)
        self.bandwidth = val

    def __get_bandwidth(self):
        val = dict()
        val["tot_in_Ko"]    = self.m.get_net_in() / 1024
        val["tot_out_Ko"]   = self.m.get_net_out()  / 1024
        val["in_Ko"]    = self.m.get_netload_in() / 1024
        val["out_Ko"]   = self.m.get_netload_out()  / 1024

        val["loc_Ko"]   = self.m.get_netload_loc() / 1024
        val["Ko"]       = val["in_Ko"] + val["out_Ko"] + val["loc_Ko"]
        return val

    def __diff_bandwidth(self, new):
        diff = True
        # old = self.bandwidth
        # if old["in_Ko"] == new["in_Ko"]\
        #     and old["out_Ko"] == new["out_Ko"]\
        #     and old["loc_Ko"] == new["loc_Ko"]:
        #     diff = True
        return diff

    # IP List managment
    def __update_iplist(self):
        if self.iplist["start"] >= len(self.iplist["iplist"]):
            self.iplist     = self.__get_iplist()

        l = len(self.iplist["iplist"])
        s = self.iplist["start"]
        if l > 0:
            val = dict()
            if (time.time() - self.time["timeiptop"]) > TIME_UPDATE_IPTOP :
                val["iptop"] = self.datanet.get_ip_list_outside_top(maxip = 10)
                self.time["timeiptop"] = time.time()
                
            val['iplist'] = self.iplist["iplist"][s:(s+MAX_IP_LIST_SEND)]
            self.cl.send(WSSUBPROT_IPLIST, val)
            self.iplist["start"] += MAX_IP_LIST_SEND

    def __get_iplist(self):
        val = dict()
        val["iplist"] = self.datanet.get_ip_list_outside()
        val["start"] = 0

        return val

    def __diff_iplist(self, new):
        diff = True

        return diff

    # Protocols List managment
    def __update_protocols(self):

        if (time.time() - self.time["protocols"]) > TIME_UPDATE_PROTOCOLS :
            self.time["protocols"] = time.time()
            val = self.__get_protocols()
            self.cl.send(WSSUBPROT_PROTOCOLS, val)


    def __get_protocols(self):
        val = dict()
        val["ethernet"] = self.datanet.get_ethertype()
        val["ip"] = self.datanet.get_IPtype()

        return val


    # Alert managment
    def __update_alert(self):
        val = self.__get_alert()
        if self.__diff_alert(val):
            self.cl.send(WSSUBPROT_ALERT, val)
        self.alert = val

    def __get_alert(self):
        val = dict()
        return val

    def __diff_alert(self, new):
        diff = True

        return diff

