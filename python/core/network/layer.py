#encoding: utf-8

"""
Network Layer

@author: Olivier BLIN
"""


class Layer():
    def __init__(self, pktdata=None, protocol=None):
        self.protocol = protocol
        self.payload = pktdata
        self.type = -1

    def __str__(self):
        if self.protocol is None:
            return "-> ROW"
        else:
            if self.payload is not None:
                return "-> "+self.protocol+" "+self.payload.__str__()
            else:
                return "-> "+self.protocol


    def get_data(self):
        return self.payload

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
                return self.payload
            else:
                return None
        else:
            return None