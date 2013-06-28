#encoding: utf-8

"""
main module for monitoring

@author: Olivier BLIN
"""

import threading, time, Queue
import multiprocessing as mp

import log, logging

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

        logger = logging.getLogger(__name__)
        logger.info("-%i-" % nb)


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

    def __init__(self):
        mp.Process.__init__(self)

        # stop condition
        self.Terminated = mp.Value('i', 0)


    def stop(self):
        self.Terminated.value = 1

    def run(self):
        logger = logging.getLogger(__name__)
        
        a = time.time()
        term = self.Terminated
        nb = 0
        while not term.value:
            nb += 1
            # logger.info("nb : %i" % nb)

        logger.info("nb : %i - time : %d" % (nb, time.time() - a))
        # print "-%i-" % nb
        # print "time : ", time.time() - a


if __name__ == "__main__":
    log.conf_logger()
    logger = logging.getLogger(__name__)

    # m = ModP()

    # logger.info("start")

    # m.start()
    # time.sleep(5)

    # m.stop()
    # m.join()

    # logger.info("stop")


    # TEST 8 * SAME THREAD
    nbth = 8
    l = list()
    for i in range(nbth):
        l.append(ModP())


    logger.info("start")
    for i in range(nbth):
        l[i].start()

    time.sleep(5)

    for i in range(nbth):
        l[i].stop()

    for i in range(nbth):
        l[i].join()

    logger.info("stop")