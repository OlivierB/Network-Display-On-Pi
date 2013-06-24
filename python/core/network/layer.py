#encoding: utf-8

"""
Network Layer

@author: Olivier BLIN
"""


class Layer():
    def __init__(self, pktdata=None, protocol=None):
        self.protocol = protocol
        self.payload = pktdata

    def __str__(self):
        if self.protocol == None:
            return "-> ROW"
        else:
            if self.payload != None:
                return "-> "+self.protocol+" "+self.payload.__str__()
            else:
                return "-> "+self.protocol

    def get_protocol(self):
        return self.protocol

    def get_pktdata(self):
        return self.payload

