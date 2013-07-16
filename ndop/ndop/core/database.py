# encoding: utf-8

"""
Client system sniffer

Use MySQLdb

@author: Olivier BLIN
"""

# Python lib import
import logging
import warnings
import MySQLdb as mdb


class Database():
    def __init__(self, host, user, passwd, database, port, maxtry=1):
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
        pass

    def execute(self, data):
        pass

    def commit(self):
        pass

    def is_connect(self):
        return self.connect is not None

    def close(self):
        pass


def fxn():
    warnings.warn("deprecated", DeprecationWarning)


class MySQL_database(Database):

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

    def execute(self, *args, **kwargs):
        if self.connect:
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    fxn()
                    cur = self.connect.cursor()
                    res = cur.execute(*args, **kwargs)
                    cur.close()
                    return res
            except mdb.Error, e:
                self.logger.error("MySQLdb Error %d: %s" % (e.args[0], e.args[1]))

    def commit(self):
        self.execute("COMMIT;")

    def close(self):
        if self.connect:
            self.connect.close()
            self.logger.debug("MySQLdb close")



