# encoding: utf-8

"""
Main module class

New submodule need to override some of these methods

@author: Olivier BLIN
"""

# Python lib import
from time import time
import datetime
import logging

class NetModule(object):

    """
    Module main class
    Define most usefull inheritance functions
    """
    def __init__(self, updatetime=10, savecode=('m', 30), protocol=None, savebdd=True, dev="lo"):

        # protocol (or module name)
        self.protocol = protocol

        # Time management for update function
        self.updatetime = updatetime
        self.lastupdate = time()

        # Time management for save function
        self.save_timecode(savecode)
        self.save_timewait()
        self.savebdd = savebdd

        self.logger = logging.getLogger()

        self.dev = dev

        # Variables List you can change
        self.l_vars = ["protocol", "updatetime", "savebdd", "savecode"]

    def __str__(self):
        return self.protocol

    def set_config(self, config=dict()):
        for elem, value in config.iteritems():
            if elem in self.l_vars:
                setattr(self, elem, value)

        self.save_timecode(self.savecode)
        self.save_timewait()

    def add_conf_override(self, elem):
        self.l_vars.append(elem)

    def trigger_data_update(self):
        """
        Manage call to update method with updatetime
        """
        if (time() - self.lastupdate) > self.updatetime:
            self.lastupdate = time()
            return self.update()

    def trigger_db_save(self, db_class):
        """
        Manage call to database_save method with savetime
        """
        if self.savebdd and time() - self.savetime > self.savewait:
            self.save_timewait()
            self.database_save(db_class)

    def save_timewait(self):
        """
        Calculate new time to wait before call to save method
        """
        if self.savecode[0] == 'm':
            d = datetime.datetime.today()
            self.savetime = time()
            self.savewait = (self.savecode[1] - (d.minute % self.savecode[1])) * 60 - d.second
        elif self.savecode[0] == 'h':
            d = datetime.datetime.today()
            self.savetime = time()
            self.savewait = (self.savecode[1] - (d.hour % self.savecode[1])) * 3600 - (d.minute * 60) - d.second
        else:
            self.savetime = time()
            self.savewait = 30 * 60
            print "NetModule : Time save error"

    def save_timecode(self, savetime):
        """
        Check savetime value and correct it if necessary
        """
        if (type(savetime) is tuple or type(savetime) is list) and len(savetime) == 2:

            if savetime[0] == 'h':
                # hours management
                if savetime[1] < 1:
                    self.savecode = ('h', 1)
                elif savetime[1] > 24:
                    self.savecode = ('h', 24)
                elif 24 % savetime[1] != 0:
                    val = int(24 / round(24 / (savetime[1] * 1.0)))
                    self.savecode = ('h', val)
                else:
                    self.savecode = ('h', savetime[1])
            else:
                # minutes management
                if savetime[1] < 1:
                    self.savecode = ('m', 1)
                elif savetime[1] > 60:
                    self.savecode = ('m', 60)
                elif 60 % savetime[1] != 0:
                    val = int(60 / round(60 / (savetime[1] * 1.0)))
                    self.savecode = ('m', val)
                else:
                    self.savecode = ('m', savetime[1])
        else:
            # default if error
            self.savecode = ('m', 30)

    def pkt_handler(self, pkt):
        """
        Called by sniffer when a new packet arrive

        pkt is formated with Packet class

        override this method
        """
        pass

    def flow_handler(self, flow):
        """
        Called by sniffer when a new flow of packets arrive

        pkt is formated with flow class

        override this method
        """
        pass

    def update(self):
        """
        Refresh method called every updatetime

        Return values to send to clients (websockets)
        automatically converted in json

        override this method
        """
        return None

    def database_init(self, db_class):
        """
        Clalled to init module database

        override this method
        """
        pass

    def database_save(self, db_class):
        """
        Called to save module data in sql database every savetime

        return a list of sql request to save module content
            else return None

        override this method
        """
        pass
