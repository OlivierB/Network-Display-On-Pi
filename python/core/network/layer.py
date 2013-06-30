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
        if self.protocol is None:
            return "-> ROW"
        else:
            if self.payload is not None:
                return "-> "+self.protocol+" "+self.payload.__str__()
            else:
                return "-> "+self.protocol

    def get_protocol(self):
        return self.protocol

    def get_data(self):
        return self.payload
