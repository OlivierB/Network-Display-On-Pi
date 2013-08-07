# -*- coding: utf-8 -*-

"""
Client system sniffer

Use netflow system

light way to sniff network

@author: Olivier BLIN
"""

import sys
import pcap
import socket
import flowtools
import logging
import threading
from time import time
from ndop.core.wsserver import WsData


SOCKET_BUFFER = 1500
SOCKET_TIMEOUT = 0.2
# Time to check modules update
MIN_TIME_MOD_UPDATE = 0.5
# Time to check modules database saving
MIN_TIME_DB_UPDATE = 10


class NetFlowSniffer(threading.Thread):

    """
    Wait results on socket
    """
    def __init__(self, config):
        threading.Thread.__init__(self)

        self.term = False

        self.config = config

        self.lmod = config.l_flowmods


    def run(self):
        # no module, no start
        if len(self.lmod) == 0:
            logger.debug("No Flow module")
            return 0

        logger = logging.getLogger()

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM)

        sock.bind((self.config.flow_addr, self.config.flow_port))
        sock.settimeout(SOCKET_TIMEOUT)

        lmod = self.lmod
        lfnt_flowhandle = list()
        for mod in lmod:
            lfnt_flowhandle.append(mod.flow_handler)

        # List loaded module
        for mod in self.lmod:
            logger.info("NetFlow : Load network module - websocket subprotocol " + mod.__str__())


        # Init
        ws_data = WsData()
        last_update_t = time()
        last_save_t = time()

        while not self.term:

            try:
                data, addr = sock.recvfrom(SOCKET_BUFFER)
                sett = flowtools.FlowPDU(pcap.aton(addr[0]), data)

                map(lambda x: map(lambda y: y(x), lfnt_flowhandle), sett)


            except socket.timeout:
                pass
            except SystemError:
                logger.error("SystemError on Flow packet")

            # Modules update call
            if time() - last_update_t > MIN_TIME_MOD_UPDATE:
                last_update_t = time()
                l_res = list()
                for mod in lmod:
                    data = mod.trigger_data_update()
                    if data is not None:
                        ws_data.send(mod.protocol, data)


    def stop(self):
        self.term = True


def printAttr( flow, attr, raw = 0 ):
    try:
        if not raw:
            val1 = eval( "flow." + attr )
            val2 = ""
        else:
            val1 = eval( "flow." + attr )
            val2 = "(0x%lx)"  % eval( "flow." + attr + "_raw" )

        print "%15s" % attr, val1, val2
    except flowtools.Error:
        pass


def printset(sett):

    try:    
        for flow in sett:
            printAttr( flow, "dFlows" )
            printAttr( flow, "dOctets" )
            printAttr( flow, "dPkts" )
            printAttr( flow, "dst_as" )
            printAttr( flow, "dst_mask" )
            printAttr( flow, "dst_tag" )
            printAttr( flow, "dstaddr", 1 )
            printAttr( flow, "dstport" )
            printAttr( flow, "engine_id" )
            printAttr( flow, "engine_type" )
            printAttr( flow, "exaddr", 1 )
            printAttr( flow, "extra_pkts" )
            printAttr( flow, "first", 1 )
            printAttr( flow, "in_encaps" )
            printAttr( flow, "input" )
            printAttr( flow, "last", 1 )
            printAttr( flow, "marked_tos" )
            printAttr( flow, "nexthop", 1 )
            printAttr( flow, "out_encaps" )
            printAttr( flow, "output" )
            printAttr( flow, "peer_nexthop", 1 )
            printAttr( flow, "prot" )
            printAttr( flow, "router_sc" )
            printAttr( flow, "src_as" )
            printAttr( flow, "src_mask" )
            printAttr( flow, "src_tag" )
            printAttr( flow, "srcaddr", 1 )
            printAttr( flow, "srcport" )
            printAttr( flow, "sysUpTime" )
            printAttr( flow, "tcp_flags" )
            printAttr( flow, "tos" )
            printAttr( flow, "unix_nsecs" )
            printAttr( flow, "unix_secs" )

    except IOError, e:
        if e.errno != errno.EPIPE:
            sys.stderr.write(e) 

