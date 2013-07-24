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
    def __init__(self, updatetime=10, savetime=('m', 30), protocol=None, dev="lo"):

        # protocol (or module name)
        self.protocol = protocol

        # Time management for update function
        self.updatetime = updatetime
        self.lastupdate = time()

        # Time management for save function
        self.save_timecode(savetime)
        self.save_timewait()

        self.logger = logging.getLogger()

        self.dev = dev

    def __str__(self):
        return self.protocol

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
        if time() - self.savetime > self.savewait:
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
        if type(savetime) is tuple and len(savetime) == 2:
            if savetime[0] == 'h':
                # hours management
                if savetime[1] < 1:
                    self.savecode = ('h', 1)
                elif savetime[1] > 24:
                    self.savecode = ('h', 24)
                else:
                    self.savecode = ('h', savetime[1])
            else:
                # minutes management
                if savetime[1] < 1:
                    self.savecode = ('m', 1)
                elif savetime[1] > 60:
                    self.savecode = ('m', 60)
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
