# encoding: utf-8

"""
Skeleton

inherit from NetModule

@author: Olivier BLIN
"""

# Project file import
from netmodule import NetModule


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
                if len(res.data) > header_end + 2:
                    info = res.data[header_end + 2:]
                    find = False
                    infoSearch = info.lower()
                    for word in l_wd:
                        if infoSearch.find(word) != -1:
                            find = True
                            break

                    if find:
                        print info
                        print "----------"


    def database_save(self, db_class):
        """
        Called to save module data in sql database every savetime
        """
        return None


l_wd = [
    "login", "pseudo", "email", "e-mail"
    "mdp", "pass", "pwd",
]
