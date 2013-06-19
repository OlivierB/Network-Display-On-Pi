#encoding: utf-8

"""
main module for monitoring

@author: Olivier BLIN
"""

import threading, time, Queue

class NetModule(threading.Thread):
    """
    Module main class
    Define most usefull inherit functions
    """
    def __init__(self, websocket=None, updatetime=10, protocol=None):
        threading.Thread.__init__(self)

        # stop condition
        self.Terminated = False

        # packet queue
        self.queue = Queue.Queue(maxsize=1000)

        # intern variable
        self.websocket      = websocket
        self.updatetime     = updatetime
        self.protocol       = protocol
        self.lastupdate     = 0


    def stop(self):
        self.Terminated = True

    def run(self):
        while not self.Terminated:
            try:
                self.pkt_handle(self.queue.get(timeout=0.1))
            except:
                pass

            if (time.time() - self.lastupdate) > self.updatetime:
                self.update()
                self.lastupdate = time.time()



    def send(self, data):
        if self.websocket != None and self.protocol != None:
            self.websocket.send(self.protocol, data)

    def pkt_put(self, pkt):
        try:
            self.queue.put(pkt, block=False)
        except:
            pass

    def update(self):
        pass

    def pkt_handle(self, pkt):
        pass

    def reset(self):
        pass

    def save(self):
        return None

    def get_protocol(self):
        return self.protocol

