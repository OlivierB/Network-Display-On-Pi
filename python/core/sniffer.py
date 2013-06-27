#encoding: utf-8

"""
Client system sniffer

Use pcap

@author: Olivier BLIN
"""

import config.server as config

import sys, time, socket, types
import string, struct, operator
import importlib
import multiprocessing as mp
import pcap
from multiprocessing import Pipe

import core.network.packet as packet
import core.mysql as mysqldata

PCAP_PROMISCUOUS_MODE   = 1
PCAP_SNIFFER_TIMEOUT    = 300
MIN_TIME_MOD_UPDATE     = 0.5
MIN_TIME_DB_UPDATE      = 1




class Sniffer(mp.Process):
    """
    Class for packet capture

    This class some modules which analyse packets and make stats
    """
    number = 0
    def __init__(self, dev="eth0"):
        mp.Process.__init__(self)

        # stop condition
        self.Terminated = mp.Value('i', 0)

        # Var
        self.dev = dev
        # communication between packet capture (pcap) and webserver (tornado) [2 process]
        self.pipe_receiver, self.pipe_sender  = Pipe(duplex=False)

    def get_data(self):
        return self.pipe_receiver.recv()

    def stop(self):
        self.Terminated.value = 1

    def run(self):
        print "Sniffer : Capture started on", self.dev
        # Init
        term = self.Terminated      # little optimisation (local variable)
        pipe = self.pipe_sender
        lmod = load_mod(config.modules_list)
        tb = time.time()
        dbupdate = time.time()
        capture = False

        # Mysql database
        mydb = mysqldata.MySQLdata(config.db_host, config.db_user, config.db_passwd, config.db_database)
        if config.db_sql_on:
            mydb.connection()

        # Get device informations if possible (IP address assigned)
        try:
            net, mask = pcap.lookupnet(dev)
        except:
            net, mask = "192.168.1.0", "255.255.255.0"

        # Create new pcap capture object
        p = pcap.pcapObject()

        try:
            # (Dev, buffer, promiscuous mode, timeout)
            p.open_live(self.dev, 1600, PCAP_PROMISCUOUS_MODE, PCAP_SNIFFER_TIMEOUT)
            capture = True

            # Handler loop
            while not term.value:
                pkt = p.next()

                if pkt != None:
                    # Decode packet
                    pktdec = packet.Packet(pkt[0], pkt[1], pkt[2])
                    # print pktdec

                    # send pkt to modules
                    for m in lmod:
                        m.pkt_handler(pktdec)

                # Module update
                if time.time() - tb > MIN_TIME_MOD_UPDATE:
                    tb = time.time()
                    ls = list()
                    for m in lmod:
                        data = m.get_data()
                        if data != None:
                            ls.append((m.get_protocol(), data))
                    if len(ls) > 0:
                        pipe.send(ls)

                if config.db_sql_on:
                    if time.time() - dbupdate > MIN_TIME_DB_UPDATE:
                        dbupdate = time.time()
                        for m in lmod:
                            data = m.get_sql()
                            if data != None:
                                mydb.execute(data)


        except KeyboardInterrupt:
            print "Sniffer : Interruption"
        except Exception as e:
            print "Sniffer : [ERROR]", e
            raise
        finally:
            if capture:
                mydb.close()
                print "Sniffer : Capture stopped..."
                a, b, c = p.stats()
                print 'Sniffer : %d packets received, %d packets dropped, %d packets dropped by interface -' % p.stats(), b/(a*1.0+1)*100



        

def load_mod(lmod):
        """
        Load modules
        """
        # Singeton Webserver data (for websocket)
        l_modules = list()

        if len(lmod) > 0:
            print "------------------------------"
            for m in lmod:
                try:
                    # import module
                    module = importlib.import_module("modules." + m)

                    # Check module main class
                    getattr(module, "NetModChild")

                    # Create an instance
                    modclass = module.NetModChild()

                    # add module to the list
                    l_modules.append(modclass)
                    print "Load module", m

                    # except ImportError as e:
                    #     print m, ":", e
                    # except AttributeError as e:
                    #     print m, ":", e
                except Exception as e:
                    print m, ":", e
            print "------------------------------"

        return l_modules