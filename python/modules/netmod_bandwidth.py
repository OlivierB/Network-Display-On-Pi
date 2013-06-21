#encoding: utf-8

"""
Client system monitoring

Use psutil

inherit from NetModule

@author: Olivier BLIN
"""


import time, psutil

import netmodule as netmod

import core.network_utils, core.network_callback

class MyMod(netmod.NetModule):
    def __init__(self, websocket=None):
        netmod.NetModule.__init__(self, websocket=websocket, updatetime=1, protocol='bandwidth')

        if psutil.__version__ < '0.7.0':
            print "Update psutil to 0.7.1"

        
        # packet data
        self.data = dict()
        self.data["pkt_nbr"] = 0
        self.data["net_load_loc"] = 0
        self.data["net_load_in"] = 0
        self.data["net_load_out"] = 0

        # init
        self.oldValues = self.sysState()
        

    def update(self):
        # System state update
        new = self.sysState()
        self.state = self.diffState(self.oldValues, new)
        self.oldValues = new

        # get data
        val = dict()
        val["tot_in_Ko"]    = self.state["net_speed_in"] / 1024
        val["tot_out_Ko"]   = self.state["net_speed_out"]  / 1024

        val["in_Ko"]    = self.state["net_load_in"] / 1024
        val["out_Ko"]   = self.state["net_load_out"]  / 1024

        val["loc_Ko"]   = self.state["net_load_loc"] / 1024
        val["Ko"]       = val["in_Ko"] + val["out_Ko"] + val["loc_Ko"]

        # send data
        self.send(val)


    def pkt_handle(self, pkt):
        self.data["pkt_nbr"] += 1

        if pkt["Ethernet"]["EtherType"] == core.network_callback.Ether_IPv4:
            src = pkt["Ethernet"]["data"]["src"]
            dst = pkt["Ethernet"]["data"]["dst"]
            bsrc = core.network_utils.ip_is_reserved(src)
            bdst = core.network_utils.ip_is_reserved(dst)

            if bsrc and bdst:
                self.data["net_load_loc"] += pkt["pkt_len"]
            elif not bsrc and bdst:
                self.data["net_load_in"] += pkt["pkt_len"]
            elif bsrc and not bdst:
                self.data["net_load_out"] += pkt["pkt_len"]

    def sysState(self):
        """
        Get system stats
        """

        val = dict()
        val["time"]     = time.time()
        val["net_sent"] = psutil.network_io_counters(pernic=False)[0]
        val["net_recv"] = psutil.network_io_counters(pernic=False)[1]
        val["net_load_loc"] = self.data["net_load_loc"]
        val["net_load_in"]  = self.data["net_load_in"]
        val["net_load_out"] = self.data["net_load_out"]

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

        #  net data on device in o/sec
        val["net_speed_out"]    = (new["net_sent"] - old["net_sent"]) / diff
        val["net_speed_in"]     = (new["net_recv"] - old["net_recv"]) / diff
        # # net data by packet analysis
        val["net_load_loc"] = (new["net_load_loc"] - old["net_load_loc"]) / diff
        val["net_load_in"] = (new["net_load_in"] - old["net_load_in"]) / diff
        val["net_load_out"] = (new["net_load_out"] - old["net_load_out"]) / diff

        return val



if __name__ == "__main__":
    m = MyMod()

    m.start()
    print "Start for 5 seconds"
    a = time.time()
    time.sleep(5)
    print time.time() - a

    m.stop()



