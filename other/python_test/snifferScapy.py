#encoding: utf-8

"""
Client system sniffer

Use Scapy

@author: Olivier BLIN
"""

# import sys
# import string
# import time
# from threading import Thread
# import types
# import re
# from scapy.all import *

# conf.iface='eth0'
# conf.verb=0
# conf.promisc=0


from threading import Thread
from Queue import Queue, Empty
from scapy.all import *
import socket

m_iface = "eth0"
m_finished = False
m_dst = "192.168.1.137"

def print_summary(pkt):
    print pkt.summary()

def threaded_sniff_target(q):
    global m_finished
    sniff(iface = m_iface, count = 10, filter = "icmp and src {0}".format(m_dst), prn = lambda x : q.put(x))
    m_finished = True

def threaded_sniff():
    q = Queue()
    sniffer = Thread(target = threaded_sniff_target, args = (q,))
    sniffer.daemon = True
    sniffer.start()
    while (not m_finished):
        try:
            pkt = q.get(timeout = 1)
            print_summary(pkt)
        except Empty:
            pass


def sniffer_run(pkt):
    s = SnifferData()
    s.inc()

    # if s.getStop():
    #     raise None

def sniffer_stop():
    s = SnifferData()
    print s.getStop()
    return False

class Sniffer(Thread):
    """
    
    """

    def __init__(self, dev="eth1", net="192.168.1.0", mask="255.255.255.0"):
        Thread.__init__(self)
        # stop condition
        self.Terminated = False

        # param
        self.dev = dev
        self.net = net
        self.mask = mask

        # Create new pcap capture object
        self.sniff = None


    def run(self):

        print "Sniffer : Server start..."

        try:
            while not self.Terminated:
                pkt = sniff(iface = self.dev, prn = sniffer_run)


        except Exception as e:
            print "Sniffer : ", e


    def stop(self):
        self.Terminated = True
        s = SnifferData()
        s.stop()
        print 'Sniffer : Server stop... VAL :', s.get()

    def getRunning(self):
        return self.Terminated



class SnifferData(object):
    """
    Singleton class to collect packet data
    """

    # Singleton creation
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SnifferData, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    #  class values
    npd = 0
    Rsniff = False

    def inc(self):
        self.npd += 1

    def get(self):
        return self.npd

    def stop(self):
        self.Rsniff = True
    def getStop(self):
        return self.Rsniff





if __name__ == "__main__":
   
    sniffer = Sniffer()
    sniffer.start()
    try:
        while 1:
            time.sleep(1)
    except KeyboardInterrupt:
        print "Stopping..."
    finally:
        sniffer.stop()


