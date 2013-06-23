#encoding: utf-8

"""
main module for monitoring

@author: Olivier BLIN
"""

import threading, time, Queue
import multiprocessing as mp

# import core.wsserver

class Mod(threading.Thread):
    """
    Module main class
    Define most usefull inherit functions
    """
    def __init__(self, t=5):
        threading.Thread.__init__(self)

        # stop condition
        self.Terminated = False
        self.lastupdate = time.time()
        self.time = t


    def stop(self):
        self.Terminated = True

    def run(self):
        nb = 0
        while not self.Terminated:
            nb += 1

            if (time.time() - self.lastupdate) > self.time:
                self.Terminated = True

        print "-%i-" % nb

class Mod1(threading.Thread):
    """
    Module main class
    Define most usefull inherit functions
    """
    def __init__(self, t=5):
        threading.Thread.__init__(self)

        # stop condition
        self.Terminated = term
        self.lastupdate = time.time()
        self.time = t


    def stop(self):
        self.Terminated = 1

    def run(self):
        nb = 0
        while not term:
            nb += 1

            if (time.time() - self.lastupdate) > self.time:
                self.Terminated = True

        print "-%i-" % nb




class ModP(mp.Process):
    """
    Module main class
    Define most usefull inherit functions
    """
    number = 0
    def __init__(self):
        mp.Process.__init__(self)

        # stop condition
        self.Terminated = mp.Value('i', 0)

    def stop(self):
        self.Terminated.value = 1

    def run(self):
        a = time.time()
        term = self.Terminated
        nb = 0
        while not term.value:
            nb += 1


        print "-%i-" % nb
        print "time : ", time.time() - a


if __name__ == "__main__":
    m = ModP()


    print "start"
    m.start()
    time.sleep(5)

    m.stop()
    m.join()

    print "stop"


    # TEST 8 * SAME THREAD
    # nbth = 8
    # l = list()
    # for i in range(nbth):
    #     l.append(Mod())


    # print "start"
    # for i in range(nbth):
    #     l[i].start()

    # for i in range(nbth):
    #     l[i].join()

    # print "stop"