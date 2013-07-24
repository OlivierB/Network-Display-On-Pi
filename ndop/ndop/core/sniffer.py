# -*- coding: utf-8 -*-

"""
Client system sniffer

Use pcap

@author: Olivier BLIN
"""

# Python lib import
from time import time, sleep
import pcap
import logging
import threading
import multiprocessing as mp

# Project file import
from ndop.core.wsserver import WsData
from ndop.core.network.packet import Packet


# Accept all packet or not
PCAP_PROMISCUOUS_MODE = 1
# Waiting time for new packet
PCAP_SNIFFER_TIMEOUT = 300
# Packet max length for capture (memory allocation)
PCAP_PACKET_MAX_LEN = 1514
# Time to check modules update
MIN_TIME_MOD_UPDATE = 0.5
# Time to check modules database saving
MIN_TIME_DB_UPDATE = 10


class SnifferManager():

    """
    Configure and Manage sniffers
    """
    def __init__(self, config):
        self.config = config

        # websocket data
        self.ws_data = WsData()

        # sniffer list
        self.l_sniffer = list()
        # sniffer data receiver list
        self.l_sniffer_data = list()
        # state
        self.is_running = False

        # init all sniffer and data receiver
        self.init()

    def init(self):
        nb_sniff = 1
        for lmod in self.config.ll_modules:
            sniff = Sniffer(self.config.sniff_dev, lmod=lmod, database=self.config.database, id=nb_sniff)
            self.l_sniffer.append(sniff)
            self.l_sniffer_data.append(SnifferData(sniff.get_data, self.ws_data))
            nb_sniff += 1

    def start(self):
        for sniff in self.l_sniffer:
            sniff.start()
            sleep(0.3)
        for sniff_data in self.l_sniffer_data:
            sniff_data.start()

        self.is_running = True

    def stop(self):
        # Stop receiver pipe first
        # because sniffers send None data to close them
        for sniff_data in self.l_sniffer_data:
            sniff_data.stop()
        # stop sniffers
        for sniff in self.l_sniffer:
            sniff.stop()

    def join(self):
        for sniff in self.l_sniffer:
            sniff.join()


class SnifferData(threading.Thread):

    """
    Get data from sniffer
    and send them to ws server
    """
    def __init__(self, get_data_func, ws_data):
        threading.Thread.__init__(self)

        self.term = False

        self.get_data_func = get_data_func
        self.ws_data = ws_data

    def run(self):
        while not self.term:
            recv = self.get_data_func()
            if recv is not None:
                for r_data in recv:
                    self.ws_data.send(r_data[0], r_data[1])

    def stop(self):
        self.term = True


class Sniffer(mp.Process):

    """
    Class for packet capture

    This class some modules which analyse packets and make stats
    """

    def __init__(self, dev, lmod=list(), database=None, id=1):
        mp.Process.__init__(self)

        # stop condition
        self.terminated = mp.Value('i', 0)

        # Var
        self.id = id
        self.database = database
        self.dev = dev
        self.lmod = lmod

        # communication between packet capture (pcap) and webserver
        # (tornado) [2 process]
        self.pipe_receiver, self.pipe_sender = mp.Pipe(duplex=False)

    def get_data(self):
        """return communication pipe"""
        return self.pipe_receiver.recv()

    def stop(self):
        """term value and end pipe"""
        self.terminated.value = 1
        self.pipe_sender.send(None)

    def run(self):
        """Sniffer main function"""
        # Get logger
        logger = logging.getLogger()
        logger.info("Sniffer %i : Capture started on %s" % (self.id, self.dev))

        # Init
        last_update_t = time()
        last_save_t = time()
        capture = False

        # Optimizations
        db_on = self.database["on"]
        lmod = self.lmod
        term = self.terminated
        pipe_send_fnt = self.pipe_sender.send

        lfnt_pkthandle = list()
        for mod in lmod:
            lfnt_pkthandle.append(mod.pkt_handler)

        # List loaded module
        for mod in self.lmod:
            logger.info("Sniffer %i : Load network module - websocket subprotocol " % (self.id) + mod.__str__())


        
        # Mysql database
        mydb = self.database["class"](
            host=self.database["conf"]["host"],
            user=self.database["conf"]["user"],
            passwd=self.database["conf"]["passwd"],
            database=self.database["conf"]["database"],
            port=self.database["conf"]["port"])

        if db_on:
            # connection to database
            mydb.connection()

            if mydb.is_connect():
                for mod in lmod:
                    data = mod.database_init(mydb)
                mydb.commit()

        # Get device informations if possible (IP address assigned)
        try:
            net, mask = pcap.lookupnet(self.dev)
        except:
            net, mask = "192.168.1.0", "255.255.255.0"

        # Create new pcap capture object
        p = pcap.pcapObject()

        try:
            # (Dev, buffer, promiscuous mode, timeout)
            p.open_live(self.dev, PCAP_PACKET_MAX_LEN, PCAP_PROMISCUOUS_MODE, PCAP_SNIFFER_TIMEOUT)
            # keep it in an available object
            GetSniffer().set_sniffer(p)
            capture = True

            # Handler loop
            # tt = (0, 0) 
            while not term.value:
                pkt = p.next()
                
                if pkt is not None:
                    
                    # Decode packet
                    pktdec = Packet(pkt[0], pkt[1], pkt[2])
                    # a = time()
                    # send pkt to modules
                    for fnt_p in lfnt_pkthandle:
                        fnt_p(pktdec)

                    # res = time() - a
                    # a, b = tt
                    # tt = (a+res, b+1)
                    # if tt[1] > 100:
                    #     print "Time sniff :", tt[0]/tt[1], "Time Tot :", tt[0]
                    #     tt = (0,0)

                
                # Modules update call
                if time() - last_update_t > MIN_TIME_MOD_UPDATE:
                    last_update_t = time()
                    l_res = list()
                    for mod in lmod:
                        data = mod.trigger_data_update()
                        if data is not None:
                            l_res.append((mod.protocol, data))
                    # Data to send with websocket
                    if len(l_res) > 0:
                        pipe_send_fnt(l_res)

                # Modules save call
                if db_on and mydb.connect is not None:
                    if time() - last_save_t > MIN_TIME_DB_UPDATE:
                        last_save_t = time()
                        for mod in lmod:
                            mod.trigger_db_save(mydb)
                        mydb.commit()
                

        except KeyboardInterrupt:
            logger.info("Sniffer %i : Interruption signal" % self.id)
        except Exception as e:
            logger.debug("Sniffer %i :" % self.id, exc_info=True)
            # logger.error("Sniffer %i : %s" % (self.id, e.strerror))
            print e
        finally:
            if capture:
                if db_on:
                    mydb.close()
                logger.info("Sniffer %i : Capture stopped..." % self.id)
                pkt_recv, pkt_drop, pkt_devdrop = p.stats()
                if pkt_recv > 0:
                    lost = pkt_drop / (pkt_recv * 1.0) * 100
                else:
                    lost = 0.0
                logger.info('Sniffer %i : %i packets received, %i packets dropped, %i packets dropped by interface - %d%%'
                            % (self.id, pkt_recv, pkt_drop, pkt_devdrop, lost))


class GetSniffer(object):

    """
    Singleton class to access to one sniffer process

    There is one GetSniffer by process (pcap process)
    """

    # Singleton creation
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GetSniffer, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    #  class value
    sniffer = None

    def set_sniffer(self, sniffer):
        if self.sniffer is None:
            self.sniffer = sniffer

    def get_stats(self):
        if self.sniffer is not None:
            return self.sniffer.stats()
        else:
            return None
