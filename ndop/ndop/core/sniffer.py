#encoding: utf-8

"""
Client system sniffer

Use pcap

@author: Olivier BLIN
"""

# Python lib import
import time
import importlib
import pcap
import logging
import threading
import multiprocessing as mp

# Project configuration file
from ndop.config import server_conf

# Project file import
from ndop.core.wsserver import ClientsList
from ndop.core.network.packet import Packet
from ndop.core.mysql import MySQLdata


# Accept all packet or not
PCAP_PROMISCUOUS_MODE = 1
# Waiting time for new packet
PCAP_SNIFFER_TIMEOUT = 300
# Packet max length for capture (memory allocation)
PCAP_PACKET_MAX_LEN = 1514
# Time to check modules update
MIN_TIME_MOD_UPDATE = 0.5
# Time to check modules SQL database saving
MIN_TIME_DB_UPDATE = 1


class SnifferManager():
    """
    Manage some sniffers
    """
    def __init__(self, dev):
        self.dev = dev
        self.ws_data = ClientsList()
        self.l_sniffer = list()
        self.l_sniffer_data = list()

        self.init()

    def init(self):
        llmod = server_conf.modules_list
        nb_sniff = 1
        for lmod in llmod:
            if type(lmod) is list:
                sniff = Sniffer(dev=self.dev, lmod=lmod, id=nb_sniff)
                self.l_sniffer.append(sniff)
                self.l_sniffer_data.append(SnifferData(sniff.get_data, self.ws_data))
                nb_sniff += 1

    def start(self):
        for sniff in self.l_sniffer:
            sniff.start()
            time.sleep(0.5)
        for sniff_data in self.l_sniffer_data:
            sniff_data.start()

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
    
    def __init__(self, dev="eth0", lmod=list(), id=1):
        mp.Process.__init__(self)

        # stop condition
        self.terminated = mp.Value('i', 0)

        # Var
        self.dev = dev
        self.lmod = lmod
        self.id = id
        # communication between packet capture (pcap) and webserver
        # (tornado) [2 process]
        self.pipe_receiver, self.pipe_sender = mp.Pipe(duplex=False)

    def get_data(self):
        return self.pipe_receiver.recv()

    def stop(self):
        self.terminated.value = 1
        self.pipe_sender.send(None)

    def run(self):
        # Get logger
        logger = logging.getLogger()
        logger.info("Sniffer %i : Capture started on %s" % (self.id, self.dev))

        # Init
        term = self.terminated      # little optimisation (local variable)
        pipe = self.pipe_sender
        lmod = load_mod(self.lmod, self.dev, pre="Sniffer %i : " % self.id)
        last_update_t = time.time()
        last_save_t = time.time()
        capture = False

        # Mysql database
        mydb = MySQLdata(server_conf.db_host, server_conf.db_user, server_conf.db_passwd, server_conf.db_database)
        if server_conf.db_sql_on:
            mydb.connection()

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
            while not term.value:
                pkt = p.next()

                if pkt is not None:
                    # Decode packet
                    pktdec = Packet(pkt[0], pkt[1], pkt[2])

                    # send pkt to modules
                    for mod in lmod:
                        mod.pkt_handler(pktdec)

                # Modules update call
                if time.time() - last_update_t > MIN_TIME_MOD_UPDATE:
                    last_update_t = time.time()
                    l_res = list()
                    for mod in lmod:
                        data = mod.get_data()
                        if data is not None:
                            l_res.append((mod.protocol, data))
                    # Data to send with websocket
                    if len(l_res) > 0:
                        pipe.send(l_res)

                # Modules save call
                if server_conf.db_sql_on:
                    if time.time() - last_save_t > MIN_TIME_DB_UPDATE:
                        last_save_t = time.time()
                        for mod in lmod:
                            data = mod.get_sql()
                            if data is not None:
                                mydb.execute(data)

        except KeyboardInterrupt:
            logger.info("Sniffer %i : Interruption signal" % self.id)
        except Exception as e:
            logger.debug("Sniffer %i :" % self.id, exc_info=True)
            # logger.error("Sniffer %i : %s" % (self.id, e.strerror))
            print e
        finally:
            if capture:
                mydb.close()
                logger.info("Sniffer %i : Capture stopped..." % self.id)
                pkt_recv, pkt_drop, pkt_devdrop = p.stats()
                if pkt_recv > 0:
                    lost = pkt_drop / (pkt_recv * 1.0) * 100
                else:
                    lost = 0.0
                logger.info('Sniffer %i : %i packets received, %i packets dropped, %i packets dropped by interface - %d%%'
                % (self.id, pkt_recv, pkt_drop, pkt_devdrop, lost))


def load_mod(lmod, dev, pre=""):
    """
    Load modules
    """
    # Get logger
    logger = logging.getLogger()

    l_modules = list()

    if len(lmod) > 0:
        for mod in lmod:
            try:
                # import module
                module = importlib.import_module("ndop.modules." + mod)

                # Check module main class
                getattr(module, "NetModChild")

                # Create an instance
                modclass = module.NetModChild(dev=dev)

                # add module to the list
                l_modules.append(modclass)
                logger.info(pre + "Load module " + mod + " (protocol:" + modclass.protocol + ")")

            except Exception:
                logger.error(pre + "Load module " + mod + " : ", exc_info=True)

    return l_modules


class GetSniffer(object):
    """
    Singleton class to access to one process sniffer
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
