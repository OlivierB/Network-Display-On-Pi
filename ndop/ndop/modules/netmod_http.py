#encoding: utf-8

"""
Skeleton

inherit from NetModule

@author: Olivier BLIN
"""

# Project file import
from netmodule import NetModule
# import core.network.netdata as netdata


class NetModChild(NetModule):
    def __init__(self, *args, **kwargs):
        NetModule.__init__(self, updatetime=5, savetime=('m', 30), protocol='http', *args, **kwargs)

    def update(self):
        """
        Refresh method called every updatetime

        Return values to send to clients (websockets)
        automatically convert in json
        """
        return None

    def pkt_handler(self, pkt):
        """
        Called by sniffer when a new packet arrive

        pkt is formated with Packet class
        """

        res = pkt.get_protocol("Ethernet", "IPv4", "TCP", "HTTP")
        if res is not None and res.type != "":
            
            # header_end = res.payload.find("\n\r")
            # pos_start = res.payload.find("\n", 0, header_end)

            # head = res.payload[0:pos_start].split(" ")
            # print head
            # header = res.payload[pos_start+1:header_end].split("\n")
            # for h in header:
            #     print h.split(": ")

            if res.type == "POST":

                header_end = res.data.find("\n\r")
                if len(res.data) > header_end+2:
                    print res.data[header_end+2:]
                    print "----------"

    def reset(self):
        """
        Clalled to reset module
        """
        pass

    def save(self):
        """
        Called to save module data in sql database every savetime
        
        return a list of sql request to save module content
            else return None

        """
        return None
