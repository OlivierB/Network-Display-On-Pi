#encoding: utf-8

"""
Network Layer

@author: Olivier BLIN
"""


class Layer():
    def __init__(self, underlayer, pktdata, protocol=None):
        self.underlayer = underlayer
        self.payload = None
        self.protocol = protocol
        self.type = -1

        self.decode(pktdata)

    def __str__(self):
        if self.protocol is None:
            return "-> ROW"
        else:
            if self.payload is not None:
                return "-> "+self.protocol+" "+self.payload.__str__()
            else:
                return "-> "+self.protocol

    def decode(self, pktdata):
        # self.data = pktdata
        pass

    def is_protocol(self, *args):
        if len(args) > 0:
            if args[0] == "*" or args[0] == self.protocol:
                if self.payload is not None:
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
                if self.payload is not None:
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

    def is_type(self, typ):
        return self.type == typ

class ProtocolMismatch(Exception):
    """Protocol error"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)