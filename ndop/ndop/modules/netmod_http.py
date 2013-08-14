# encoding: utf-8

"""
Skeleton

inherit from NetModule

Try to catch password in http post

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


l_wd = [
    "login", "pseudo", "email", "e-mail",
    "mdp", "pass", "pwd",
]
