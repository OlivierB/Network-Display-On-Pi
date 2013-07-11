# encoding: utf-8

"""
Client system sniffer

Use MySQLdb

@author: Olivier BLIN
"""

# Python lib import
import logging
import MySQLdb as mdb


class MySQLdata():

    def __init__(self, host, user, passwd, database, port=3306, maxtry=3):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database
        self.port = port
        self.maxtry = maxtry

        # Init
        self.connect = None
        self.nbrtry = 0

        # Get logger
        self.logger = logging.getLogger()

    def connection(self):
        while (not self.connect) and (self.nbrtry < self.maxtry):
            self.nbrtry += 1
            try:
                self.connect = mdb.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    passwd=self.passwd,
                    db=self.database)
            except mdb.Error, e:
                self.logger.error("Try %i - MySQLdb Error %d: %s" % (self.nbrtry, e.args[0], e.args[1]))
            finally:
                if self.connect:
                    self.logger.debug("MySQLdb connection OK")
                    self.nbrtry = 0

    def execute(self, data):
        if self.connect:
            try:
                with self.connect:
                    cur = self.connect.cursor()

                    if type(data) is list:
                        for e in data:
                            cur.execute(e)
                    else:
                        cur.execute(data)
            except mdb.Error, e:
                self.logger.error("MySQLdb Error %d: %s" % (e.args[0], e.args[1]))

    def close(self):
        if self.connect:
            self.connect.close
            self.logger.debug("MySQLdb close")
