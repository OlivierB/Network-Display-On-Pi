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
import multiprocessing as mp

# Project configuration file
import config.server as config

# Project file import
import core.network.packet as packet
import core.mysql as mysqldata


# Accept all packet or not
PCAP_PROMISCUOUS_MODE = 1
# Waiting time for new packet
PCAP_SNIFFER_TIMEOUT = 300
# Packet max length for capture
PCAP_PACKET_MAX_LEN = 1514
# Time to check modules update
MIN_TIME_MOD_UPDATE = 0.5
# Time to check modules SQL database saving
MIN_TIME_DB_UPDATE = 1


class Sniffer(mp.Process):
    """
    Class for packet capture

    This class some modules which analyse packets and make stats
    """
    
    def __init__(self, dev="eth0"):
        mp.Process.__init__(self)

        # stop condition
        self.terminated = mp.Value('i', 0)

        # Var
        self.dev = dev
        # communication between packet capture (pcap) and webserver
        # (tornado) [2 process]
        self.pipe_receiver, self.pipe_sender = mp.Pipe(duplex=False)

    def get_data(self):
        return self.pipe_receiver.recv()

    def stop(self):
        self.terminated.value = 1

    def run(self):
        # Get logger
        logger = logging.getLogger()
        logger.info("Sniffer : Capture started on " + self.dev)

        # Init
        term = self.terminated      # little optimisation (local variable)
        pipe = self.pipe_sender
        lmod = load_mod(config.modules_list)
        last_update_t = time.time()
        last_save_t = time.time()
        capture = False

        # Mysql database
        mydb = mysqldata.MySQLdata(config.db_host, config.db_user, config.db_passwd, config.db_database)
        if config.db_sql_on:
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
            capture = True

            # Handler loop
            while not term.value:
                pkt = p.next()

                if pkt is not None:
                    # Decode packet
                    pktdec = packet.Packet(pkt[0], pkt[1], pkt[2])

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
                if config.db_sql_on:
                    if time.time() - last_save_t > MIN_TIME_DB_UPDATE:
                        last_save_t = time.time()
                        for mod in lmod:
                            data = mod.get_sql()
                            if data is not None:
                                mydb.execute(data)

        except KeyboardInterrupt:
            logger.info("Sniffer : Interruption signal")
        except Exception:
            logger.error("Sniffer : ", exc_info=True)
        finally:
            if capture:
                mydb.close()
                logger.info("Sniffer : Capture stopped...")
                pkt_recv, pkt_drop, pkt_devdrop = p.stats()
                if pkt_recv > 0:
                    lost = pkt_drop / (pkt_recv * 1.0) * 100
                else:
                    lost = 0.0
                logger.info('Sniffer : %i packets received, %i packets dropped, %i packets dropped by interface - %d%%'
                % (pkt_recv, pkt_drop, pkt_devdrop, lost))


def load_mod(lmod):
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
                module = importlib.import_module("modules." + mod)

                # Check module main class
                getattr(module, "NetModChild")

                # Create an instance
                modclass = module.NetModChild()

                # add module to the list
                l_modules.append(modclass)
                logger.info("Load module " + mod + " (protocol:" + modclass.protocol + ")")

            except Exception:
                logger.error(mod + " : ", exc_info=True)

    return l_modules
