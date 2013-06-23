#encoding: utf-8

"""
main module for monitoring

@author: Olivier BLIN
"""

import time

# import core.wsserver

class NetModule():
    """
    Module main class
    Define most usefull inheritance functions
    """
    def __init__(self, updatetime=10, protocol=None):

        # intern variable
        self.protocol       = protocol
        self.updatetime     = updatetime
        self.lastupdate     = 0


    def update(self):
        return None

    def pkt_handler(self, pkt):
        pass

    def get_protocol(self):
        return self.protocol

    def get_data(self):
        if (time.time() - self.lastupdate) > self.updatetime:
            self.lastupdate = time.time()
            return self.update()
        else:
            return None

    def reset(self):
        pass

    def save(self):
        pass
