#encoding: utf-8

"""
main module for monitoring

@author: Olivier BLIN
"""

import threading, time, Queue
import multiprocessing as mp

class elem():
    def __init__(self, val=""):
        self.val = val

    def getVal(self):
        return self.val

    def putVal(self, val):
        self.val = val

    def pVal(self):
        print self.val


class ModT(threading.Thread):
    """
    Module main class
    Define most usefull inherit functions
    """
    def __init__(self, name, updatetime=1):
        threading.Thread.__init__(self)

        # stop condition
        self.Terminated = False

        # queue
        self.queue = Queue.Queue(maxsize=1000)
        self.updatetime     = updatetime
        self.lastupdate     = 0

        self.name = name
        self.elem = elem("Empty")

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

    def put(self, pkt):
        try:
            self.queue.put(pkt, block=False)
        except:
            pass

    def update(self):
        print self.name, ":", self.elem.getVal()

    def pkt_handle(self, pkt):
        self.elem = pkt

    def getQueue(self):
        return self.queue


class ModP(mp.Process):
    """
    Module main class
    Define most usefull inherit functions
    """
    def __init__(self, name, updatetime=1, args=()):
        mp.Process.__init__(self)

        # stop condition
        self.Terminated = False

        # queue
        self.queue = Queue.Queue(maxsize=1000)
        self.updatetime     = updatetime
        self.lastupdate     = 0

        self.name = name
        self.elem = elem("Empty")
        self.args = args

    def stop(self):
        self.Terminated = True

    def run(self):
        print "Debut"
        print self.args
        # # while not self.Terminated:
        # try:
        #     self.pkt_handle(self.queue.get(timeout=3))
        # except:
        #     pass


        # if (time.time() - self.lastupdate) > self.updatetime:
        #         self.update()
        #         self.lastupdate = time.time()
        elem = self.args.get()
        print elem.getVal()
        print self.args.get()
        print elem.getVal()
        print "fin"


    def send(self, data):
        if self.websocket != None and self.protocol != None:
            self.websocket.send(self.protocol, data)

    def put(self, pkt):
        try:
            self.queue.put(pkt, block=False)
        except:
            pass

    def update(self):
        print self.name, ":", self.elem.getVal()

    def pkt_handle(self, pkt):
        self.elem = pkt

    def getQueue(self):
        return self.queue


if __name__ == "__main__":
    queue = mp.Queue()
    e = elem("main")
    p = ModP("A", args=queue)

    p.start()
    queue.put(e)
    time.sleep(2)
    e.putVal("NAAAAAAAAAAN")
    time.sleep(2)
    queue.put("ee")
    time.sleep(2)
    p.stop()
    p.join()



    # parent_conn, child_conn2 = mp.Pipe()
    # e = elem("main")
    # p = ModP("A", args=child_conn2)

    # p.start()
    # time.sleep(2)
    # parent_conn.send(e)
    # e.putVal("NAAAAAAAAAAN")
    # parent_conn.send("ee")
    # time.sleep(2)
    # p.stop()
    # p.join()

    # th = ModT("A")
    # th2 = ModT("B")
    # e = elem("main")

    # th.start()
    # th2.start()

    # time.sleep(1)
    # th.put(e)
    # th2.put(e)
    # time.sleep(3)
    # e.putVal("mainChg")
    # time.sleep(3)
    
    # th.stop()
    # th2.stop()

