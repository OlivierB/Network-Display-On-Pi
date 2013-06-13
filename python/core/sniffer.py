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



class Sniffer(threading.Thread):
    """
    
    """

    def __init__(self, dev="eth0"):
        threading.Thread.__init__(self)
        # run stop conditions
        self.Terminated = False

        # other
        self.dev = dev
        # Create new pcap capture
        self.p = pcap.pcapObject()

        # Stat
        self.stat_nbPacket = 0


    def run(self):

        print "Sniffer : Pcap start..."

        try:
            
            # Select device
            net, mask = pcap.lookupnet(self.dev)
            # (Dev, buffer, promiscuous mode, timeout)
            self.p.open_live(self.dev, 1600, 1, 100)

            # self.p.setnonblock(1)

            while not self.Terminated:
                # time.sleep(1)
                res = self.p.next()
                if isinstance(res, types.TupleType):
                    # print self.stat_nbPacket, " --> ", res[0]
                    self.stat_nbPacket += 1


        except Exception as e:
            print "Sniffer : ", e


    def stop(self):
        self.Terminated = True

        print 'Sniffer : Pcap stop...'

        
        # print 'sniffer : %d packets received, %d packets dropped, %d packets dropped by interface' % self.p.stats()





if __name__ == "__main__":
    p = Sniffer()
    p.start()
    time.sleep(5)
    p.stop()



# protocols={ socket.IPPROTO_TCP:'tcp',
#             socket.IPPROTO_UDP:'udp',
#             socket.IPPROTO_ICMP:'icmp'}



# def decode_ip_packet(s):
#     d={}
#     d['version']=(ord(s[0]) & 0xf0) >> 4
#     d['header_len']=ord(s[0]) & 0x0f
#     d['tos']=ord(s[1])
#     d['total_len']=socket.ntohs(struct.unpack('H',s[2:4])[0])
#     d['id']=socket.ntohs(struct.unpack('H',s[4:6])[0])
#     d['flags']=(ord(s[6]) & 0xe0) >> 5
#     d['fragment_offset']=socket.ntohs(struct.unpack('H',s[6:8])[0] & 0x1f)
#     d['ttl']=ord(s[8])
#     d['protocol']=ord(s[9])
#     d['checksum']=socket.ntohs(struct.unpack('H',s[10:12])[0])
#     d['source_address']=pcap.ntoa(struct.unpack('i',s[12:16])[0])
#     d['destination_address']=pcap.ntoa(struct.unpack('i',s[16:20])[0])
#     if d['header_len']>5:
#         d['options']=s[20:4*(d['header_len']-5)]
#     else:
#         d['options']=None
#     d['data']=s[4*d['header_len']:]
#     return d


# def dumphex(s):
#     bytes = map(lambda x: '%.2x' % x, map(ord, s))
#     for i in xrange(0,len(bytes)/16):
#         print '    %s' % string.join(bytes[i*16:(i+1)*16],' ')
#     print '    %s' % string.join(bytes[(i+1)*16:],' ')
            

def print_packet(pktlen, data, timestamp):
    if not data:
        return

    if data[12:14]=='\x08\x00':
        # decoded=decode_ip_packet(data[14:])
        # print '\n%s.%f %s > %s' % (time.strftime('%H:%M',
        #                                                                              time.localtime(timestamp)),
        #                                                  timestamp % 60,
        #                                                  decoded['source_address'],
        #                                                  decoded['destination_address'])
        # for key in ['version', 'header_len', 'tos', 'total_len', 'id',
        #                         'flags', 'fragment_offset', 'ttl']:
        #     print '  %s: %d' % (key, decoded[key])
        # print '  protocol: %s' % protocols[decoded['protocol']]
        # print '  header checksum: %d' % decoded['checksum']
        # print '  data:'
        # dumphex(decoded['data'])
        # print "b"
        return
 




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

