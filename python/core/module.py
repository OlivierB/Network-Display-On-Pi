#encoding: utf-8

"""
First module for monitoring

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
        self.queue = Queue.Queue(maxsize=100)

        # intern variable
        self.websocket = websocket
        self.updatetime = updatetime
        self.protocol = protocol


    def stop(self):
        self.Terminated = True

    def run(self):
        try:
            while not self.Terminated:
                time.sleep(1)
        except:
            pass
        finally:
            self.stop()

    def send(self, data):
        if self.websocket != None:
            self.websocket.send(self.protocol, data)

    def pkt_put(self, pkt):
        try:
            self.queue.put(pkt, block=False)
        except:
            pass



class MyMod(NetModule):
    def __init__(self):
        NetModule.__init__(self)

    def isRunning(self):
        return not self.Terminated



if __name__ == "__main__":
    m = MyMod()
    print m.start()
    time.sleep(5)
    print m.stop()


