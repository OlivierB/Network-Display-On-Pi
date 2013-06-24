#encoding: utf-8

"""
Network implementation data

@author: Olivier BLIN
"""

import pcap

dIPReserved = [
    (pcap.aton('0.0.0.0'), 8),        # Current network (only valid as source address)  RFC 5735
    (pcap.aton('10.0.0.0'), 8),       # Private network RFC 1918
    (pcap.aton('100.64.0.0'), 10),    # Shared Address Space    RFC 6598
    (pcap.aton('127.0.0.0'), 8),      # Loopback    RFC 5735
    (pcap.aton('169.254.0.0'), 16),   # Link-local  RFC 3927
    (pcap.aton('172.16.0.0'), 12),    # Private network RFC 1918
    (pcap.aton('192.0.0.0'), 24),     # IETF Protocol Assignments   RFC 5735
    (pcap.aton('192.0.2.0'), 24),     # TEST-NET-1, documentation and examples  RFC 5735
    (pcap.aton('192.88.99.0'), 24),   # IPv6 to IPv4 relay  RFC 3068
    (pcap.aton('192.168.0.0'), 16),   # Private network RFC 1918
    (pcap.aton('198.18.0.0'), 15),    # Network benchmark tests RFC 2544
    (pcap.aton('198.51.100.0'), 24),  # TEST-NET-2, documentation and examples  RFC 5737
    (pcap.aton('203.0.113.0'), 24),   # TEST-NET-3, documentation and examples  RFC 5737
    (pcap.aton('224.0.0.0'), 4),      # IP multicast (former Class D network)   RFC 5771
    (pcap.aton('240.0.0.0'), 4),      # Reserved (former Class E network)   RFC 1700
    (pcap.aton('255.255.255.255'), 32)# Broadcast
]
