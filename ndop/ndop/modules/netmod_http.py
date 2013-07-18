# encoding: utf-8

"""
Skeleton

inherit from NetModule

@author: Olivier BLIN
"""


import pcap

# Project file import
from netmodule import NetModule


class NetModChild(NetModule):

    def __init__(self, *args, **kwargs):
        NetModule.__init__(self, updatetime=5, savetime=('m', 30), protocol='http', *args, **kwargs)

        self.last = list()

    def update(self):

        val = dict()
        val["info"] = self.last

        return val

    def pkt_handler(self, pkt):

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
                    lres = list()
                    for word in l_wd:
                        pos = infoSearch.find(word)
                        if pos != -1:
                            find = True
                            lres.append(pos)

                    if find:
                        val = dict()
                        val["src"] = pcap.ntoa(pkt.Ether.payload.src)
                        val["dst"] = pcap.ntoa(pkt.Ether.payload.dst)
                        val["res"] = list()
                        for pos in lres:
                            val["res"].append(info[pos:pos+50])


                        self.last.append(val)
                        if len(self.last) > 1000:
                            self.last.pop(0)



    def database_save(self, db_class):
        """
        Called to save module data in sql database every savetime
        """
        return None


l_wd = [
    "login", "pseudo", "email", "e-mail",
    "mdp", "pass", "pwd",
]
