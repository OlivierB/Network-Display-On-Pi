#encoding: utf-8

"""
Network utils

@author: Olivier BLIN
"""

import struct

class Packet():
    def __init__(self, pktlen=0, pktdata=None, timestamp=0):
        self.timestamp = timestamp
        self.pktlen = pktlen
        self.packet = Ethernet(pktdata)

    def __str__(self):
        tor = "< len : " + str(self.pktlen)
        tor += " - time : " + str(self.timestamp)
        tor += " " + self.packet.__str__()
        tor += " >"
        return tor

    def get_time(self):
        return self.timestamp

    def get_len(self):
        return self.pktlen

    def get_pkt(self):
        return self.pktlen


class Layer():
    def __init__(self, pktdata=None, protocol=None):
        self.protocol = protocol
        self.layer_header = None
        self.layer_data = pktdata
        self.error = False

    def __str__(self):
        if self.protocol == None:
            return "-> DATA"
        else:
            return "-> "+self.protocol

    def get_protocol(self):
        return self.protocol

    def get_pktdata(self):
        return self.pktdata

    def is_error(self):
        self.error


class Ethernet(Layer):
    def __init__(self, pktdata):
        Layer.__init__(self, protocol="Ethernet")
        self.layer_header = pktdata[0:14]
        self.layer_data = Layer(pktdata[14:])

    def __str__(self):
        tor = "[Ethernet " + self.layer_data.__str__() + "]"
        return tor

    def get_macsrc(self):
        return self.layer_data[0:6]

    def get_macdst(self):
        return self.layer_data[6:12]

    def get_macsrc_s(self):
        return mac_to_string(self.layer_data[0:6])

    def get_macdst_s(self):
        return mac_to_string(self.layer_data[6:12])


def mac_to_string(data):
    s = ""
    for i in range(6):
        tmp = "%x" % struct.unpack("B", data[i])
        while len(tmp) < 2:
            tmp = "0"+tmp
        s += tmp
        if i < 5:
            s += ":"
    return s


    # # Ethernet protocol decode
    # typ = pktdata[12:14]
    # pkt["EtherType"] = typ
    # if typ in core.network_callback.dEtherType.keys()\
    #     and core.network_callback.dEtherType[typ]["callback"] != None:
    #         pkt["data"] = core.network_callback.dEtherType[typ]["callback"](pktdata[14:])
    # else:
    #     pkt["data"] = pktdata
    
    # return pkt
