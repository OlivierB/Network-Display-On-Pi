#encoding: utf-8

"""
Network Layer

@author: Olivier BLIN
"""


class Layer():
    def __init__(self, pktdata=None, protocol=None, start=0):
        self.protocol = protocol
        self.payload = pktdata
        self.start = start
        self.type = -1

        self.decode()

    def __str__(self):
        if self.protocol is None:
            return "-> ROW"
        else:
            if self.payload is not None:
                return "-> "+self.protocol+" "+self.payload.__str__()
            else:
                return "-> "+self.protocol

    def decode(self):
        pass

    def data(self, start=None):
        if start is not None:
            return self.payload[self.start+start:]
        return self.payload[self.start:]

    def range(self, start, end):
        return self.payload[self.start+start:self.start+end]

    def rangeN(self, start, nb):
        pos = self.start+start
        return self.payload[pos:pos+nb]

    def at(self, pos):
        return self.payload[self.start+pos]

    def is_protocol(self, *args):
        if len(args) > 0:
            if args[0] == "*" or args[0] == self.protocol:
                if self.protocol is not None:
                    return self.payload.is_protocol(*args[1:])
                else:
                    return False
            else:
                return False
        else:
            return True

    def get_protocol(self, *args):
        if len(args) > 1:
            if args[0] == "*" or args[0] == self.protocol:
                if self.protocol is not None:
                    return self.payload.get_protocol(*args[1:])
                else:
                    return None
            else:
                return None
        elif len(args) == 1:
            if args[0] == "*" or args[0] == self.protocol:
                return self
            else:
                return None
        else:
            return None
