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

import config.network

def decode_ip_packet(s):
    d={}
    d['version']=(ord(s[0]) & 0xf0) >> 4
    d['header_len']=ord(s[0]) & 0x0f
    d['tos']=ord(s[1])
    d['total_len']=socket.ntohs(struct.unpack('H',s[2:4])[0])
    d['id']=socket.ntohs(struct.unpack('H',s[4:6])[0])
    d['flags']=(ord(s[6]) & 0xe0) >> 5
    d['fragment_offset']=socket.ntohs(struct.unpack('H',s[6:8])[0] & 0x1f)
    d['ttl']=ord(s[8])
    d['protocol']=ord(s[9])
    d['checksum']=socket.ntohs(struct.unpack('H',s[10:12])[0])
    d['source_address']=pcap.ntoa(struct.unpack('i',s[12:16])[0])
    d['destination_address']=pcap.ntoa(struct.unpack('i',s[16:20])[0])
    if d['header_len']>5:
        d['options']=s[20:4*(d['header_len']-5)]
    else:
        d['options']=None
    d['data']=s[4*d['header_len']:]

    return d

def dumphex(s):
    bytes = map(lambda x: '%.2x' % x, map(ord, s))
    for i in xrange(0,len(bytes)/16):
        print '    %s' % string.join(bytes[i*16:(i+1)*16],' ')
    print '    %s' % string.join(bytes[(i+1)*16:],' ')
            
def print_packet(pktlen, data, timestamp):
    if not data:
        return

    if data[12:14]=='\x08\x00':
        decoded=decode_ip_packet(data[14:])
        print '\n%s.%f %s > %s' % ( time.strftime('%H:%M',
                                    time.localtime(timestamp)),
                                    timestamp % 60,
                                    decoded['source_address'],
                                    decoded['destination_address'])
        for key in ['version', 'header_len', 'tos', 'total_len', 'id',
                                'flags', 'fragment_offset', 'ttl']:
            print '  %s: %d' % (key, decoded[key])

        print '  protocol: %s' % decoded['protocol']
        print '  header checksum: %d' % decoded['checksum']
        print '  pkt len : ', pktlen
        print '  data:'
        dumphex(decoded['data'])
        return




class Sniffer(threading.Thread):
    """
    
    """

    def __init__(self, dev="eth0", net="192.168.1.0", mask="255.255.255.0"):
        threading.Thread.__init__(self)
        # stop condition
        self.Terminated = False

        # Data
        self.ET = config.network.dEtherType
        self.IPT = config.network.dIPType

        # param
        self.dev = dev
        self.net = net
        self.mask = mask

        # Create new pcap capture object
        self.p = pcap.pcapObject()

        # Stat


    def run(self):

        print "Sniffer : Pcap start..."
        print self.dev

        try:
            # Get device informations if possible (IP address assigned)
            try:
                net, mask = pcap.lookupnet(self.dev)
                self.net = pcap.ntoa(net)
                self.mask = pcap.ntoa(mask)
            except:
                pass


            # (Dev, buffer, promiscuous mode, timeout)
            self.p.open_live(self.dev, 1600, 0, 100)


            while not self.Terminated:
                # return tuple : pktlen, data, timestamp
                res = self.p.next()
                if isinstance(res, types.TupleType):
                    self.packet_analyse(res)


        except Exception as e:
            print "Sniffer : ", e


    def stop(self):
        self.Terminated = True

        print 'Sniffer : Pcap stop...'
        print 'sniffer : %d packets received, %d packets dropped, %d packets dropped by interface' % self.p.stats()


    def packet_analyse(self, pkt):
        # p = decode_ip_packet(pkt[1])
        # print "--> ", pkt[0], " ", decode_ip_packet(pkt[1])["total_len"], " ", decode_ip_packet(pkt[1])["header_len"]

        # pktlen, data, timestamp
        v = pkt[1][12:14]
        if v in self.ET.keys():
            print self.ET[v]["protocol"]

        # if pkt[1][12:14]=='\x08\x00':
        #     print "IP"
        # elif pkt[1][12:14]=='\x08\x06':
        #     print "ARP"
        # elif pkt[1][12:14]=='\x80\x35':
        #     print "RARP"
        # else:
        #     print "Unknow"
        # return


if __name__ == "__main__":
    p = Sniffer()
    p.start()
    try:
        while 1:
            time.sleep(1)
    except KeyboardInterrupt:
        print "Stopping..."
    finally:
        p.stop()




 




    # if __name__=='__main__':

    #     if len(sys.argv) < 3:
    #         print 'usage: sniff.py <interface> <expr>'
    #         sys.exit(0)
    #     p = pcap.pcapObject()
    #     #dev = pcap.lookupdev()
    #     dev = sys.argv[1]
    #     net, mask = pcap.lookupnet(dev)

    #     # note:  to_ms does nothing on linux
    #     p.open_live(dev, 1600, 1, 100)
    #     #p.dump_open('dumpfile')
    #     p.setfilter(string.join(sys.argv[2:],' '), 0, 0)

    #     # try-except block to catch keyboard interrupt.  Failure to shut
    #     # down cleanly can result in the interface not being taken out of promisc.
    #     # mode
    #     #p.setnonblock(1)
    #     try:
    #         while 1:
    #             p.dispatch(1, print_packet)

    #         # specify 'None' to dump to dumpfile, assuming you have called
    #         # the dump_open method
    #         #  p.dispatch(0, None)

    #         # the loop method is another way of doing things
    #         #  p.loop(1, print_packet)

    #         # as is the next() method
    #         # p.next() returns a (pktlen, data, timestamp) tuple 
    #         #  apply(print_packet,p.next())
    #     except KeyboardInterrupt:
    #         print '%s' % sys.exc_type
    #         print 'shutting down'
    #         print '%d packets received, %d packets dropped, %d packets dropped by interface' % p.stats()




"""
0x0800  Internet Protocol version 4 (IPv4)
0x0806  Address Resolution Protocol (ARP)
0x0842  Wake-on-LAN[3]
0x22F3  IETF TRILL Protocol
0x6003  DECnet Phase IV
0x8035  Reverse Address Resolution Protocol
0x809B  AppleTalk (Ethertalk)
0x80F3  AppleTalk Address Resolution Protocol (AARP)
0x8100  VLAN-tagged frame (IEEE 802.1Q) & Shortest Path Bridging IEEE 802.1aq[4]
0x8137  IPX
0x8138  IPX
0x8204  QNX Qnet
0x86DD  Internet Protocol Version 6 (IPv6)
0x8808  Ethernet flow control
0x8809  Slow Protocols (IEEE 802.3)
0x8819  CobraNet
0x8847  MPLS unicast
0x8848  MPLS multicast
0x8863  PPPoE Discovery Stage
0x8864  PPPoE Session Stage
0x8870  Jumbo Frames
0x887B  HomePlug 1.0 MME
0x888E  EAP over LAN (IEEE 802.1X)
0x8892  PROFINET Protocol
0x889A  HyperSCSI (SCSI over Ethernet)
0x88A2  ATA over Ethernet
0x88A4  EtherCAT Protocol
0x88A8  Provider Bridging (IEEE 802.1ad) & Shortest Path Bridging IEEE 802.1aq[5]
0x88AB  Ethernet Powerlink[citation needed]
0x88CC  Link Layer Discovery Protocol (LLDP)
0x88CD  SERCOS III
0x88E1  HomePlug AV MME[citation needed]
0x88E3  Media Redundancy Protocol (IEC62439-2)
0x88E5  MAC security (IEEE 802.1AE)
0x88F7  Precision Time Protocol (IEEE 1588)
0x8902  IEEE 802.1ag Connectivity Fault Management (CFM) Protocol / ITU-T Recommendation Y.1731 (OAM)
0x8906  Fibre Channel over Ethernet (FCoE)
0x8914  FCoE Initialization Protocol
0x8915  RDMA over Converged Ethernet (RoCE)
0x892F  High-availability Seamless Redundancy (HSR)
0x9000  Ethernet Configuration Testing Protocol[6]
0x9100  Q-in-Q
0xCAFE  Veritas Low Latency Transport (LLT)[7] for Veritas Cluster Server
"""

