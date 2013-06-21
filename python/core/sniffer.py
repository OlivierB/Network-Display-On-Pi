#encoding: utf-8

"""
Client system sniffer

Use pcap

@author: Olivier BLIN
"""

import pcap
import sys
import string
import time
import threading
import socket
import struct
import types
import operator

import core.network_callback
import core.network_utils
import core.netmod_manager
import core.packet

PCAP_PROMISCUOUS_MODE   = 1


class Sniffer(threading.Thread):
    """
    Class for packet capture

    This class send packet in module's queue
    """

    def __init__(self, dev="eth0", net="192.168.1.0", mask="255.255.255.0"):
        threading.Thread.__init__(self)
        # stop condition
        self.Terminated = False

        # param
        self.dev = dev
        self.net = net
        self.mask = mask

        # Create new pcap capture object
        self.p = pcap.pcapObject()

        # Modules list
        self.lmod = core.netmod_manager.NetmodManager()


    def run(self):

        print "Sniffer : Pcap start on %s..." % self.dev

        # time.sleep(1)

        try:
            # Get device informations if possible (IP address assigned)
            try:
                net, mask = pcap.lookupnet(self.dev)
                self.net = pcap.ntoa(net)
                self.mask = pcap.ntoa(mask)
            except:
                pass

            # (Dev, buffer, promiscuous mode, timeout)
            self.p.open_live(self.dev, 1600, PCAP_PROMISCUOUS_MODE, 100)

            while not self.Terminated:
                # return tuple : pktlen, data, timestamp
                pkt = self.p.next()
                if isinstance(pkt, types.TupleType):
                    pktdec = core.network_utils.packet_decode(pkt[0], pkt[1], pkt[2])
                    # pktdec = core.packet.Packet(pkt[0], pkt[1], pkt[2])

                    # send pkt to modules
                    self.lmod.send(pktdec)


            # End
            a, b, c = self.p.stats()
            print 'sniffer : %d packets received, %d packets dropped, %d packets dropped by interface -' % self.p.stats(), b/(a*1.0+1)*100

        except Exception as e:
            print "Sniffer : ", e
            raise

    def stop(self):
        self.Terminated = True


    def stats(self):
        try:
            a, b, c = self.p.stats()
        except:
            return 0, 0, 0
        return a, b, c

        print 'Sniffer : Pcap stop...'

