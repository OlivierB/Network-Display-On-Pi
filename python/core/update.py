#encoding: utf-8

"""
System Information collector

Optimization of websocket send

@author: Olivier BLIN
"""

import core.sniffer, core.wsserver, core.monitoring

WSSUBPROT_SYSDATA       = 'server_stat'
WSSUBPROT_BANDWIDTH     = 'bandwidth'
WSSUBPROT_IPLIST        = 'iplist'


class Update():
    def __init__(self, monnitor, pcap):
        self.m = monnitor
        self.p = pcap
        self.cl = core.wsserver.ClientsList()

        # values save
        self.sysdata    = self.__get_sysdata()
        self.bandwidth  = self.__get_bandwidth()
        self.iplist     = self.__get_iplist()

    #  Global update
    def update(self):
        self.__update_sysdata()
        self.__update_bandwidth()
        self.__update_iplist()

    # Update
    def __update_sysdata(self):
        val = self.__get_sysdata()
        if self.__diff_sysdata(val):
            self.cl.send(WSSUBPROT_SYSDATA, val)
        self.sysdata = val

    def __update_bandwidth(self):
        val = self.__get_bandwidth()
        if self.__diff_bandwidth(val):
            self.cl.send(WSSUBPROT_BANDWIDTH, val)
        self.bandwidth = val

    def __update_iplist(self):
        val = self.__get_iplist()
        if self.__diff_iplist(val):
            self.cl.send(WSSUBPROT_IPLIST, val)
        self.bandwidth = val
        

    # Collect data
    def __get_sysdata(self):
        val = dict()
        val["mem_load"]     = self.m.get_mem()
        val["proc_load"]    = self.m.get_cpu()
        val["swap_load"]    = self.m.get_swap()
        return val

    def __get_bandwidth(self):
        val = dict()
        val["in_Ko"]    = self.m.get_net_in() / 1024
        val["out_Ko"]   = self.m.get_net_out()  / 1024
        val["loc_Ko"]   = 0
        val["Ko"]       = val["in_Ko"] + val["out_Ko"]
        return val

    def __get_iplist(self):
        val = dict()

        return val

    # diff state
    def __diff_sysdata(self, new):
        diff = True
        old = self.sysdata
        if old["mem_load"] == new["mem_load"]\
            and old["proc_load"] == new["proc_load"]\
            and old["swap_load"] == new["swap_load"]:
            diff = True
        return diff

    def __diff_bandwidth(self, new):
        diff = True
        # old = self.bandwidth
        # if old["in_Ko"] == new["in_Ko"]\
        #     and old["out_Ko"] == new["out_Ko"]\
        #     and old["loc_Ko"] == new["loc_Ko"]:
        #     diff = True
        return diff

    def __diff_iplist(self, new):
        diff = True

        return diff
