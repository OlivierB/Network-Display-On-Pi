#!/usr/bin/python
# -*- coding: utf-8 -*-

# import _mysql
# import sys

# con = None
# try:
#     con = _mysql.connect(
#         host="192.168.1.144", 
#         port=3306, 
#         user="ndop", 
#         passwd="ndop", 
#         db="NDOP")

#     con.query("SELECT VERSION()")
#     result = con.use_result()

#     print "MySQL version: %s" % \
#     result.fetch_row()[0]

# except _mysql.Error, e:

#     print "Error %d: %s" % (e.args[0], e.args[1])
#     sys.exit(1)

# finally:
#     if con:
#         con.close()

# import MySQLdb as mdb
# import sys
# import time
# import random

# connect = None

# def rand():
#     return str(random.randrange(0, 1000, 10))

# # try:
# connect = mdb.connect(
#         host="192.168.1.144", 
#         port=3306, 
#         user="ndop", 
#         passwd="ndop", 
#         db="NDOP")



    # a = time.time()
    # for i in range(10000):
    #     cur.execute(req)
    # print "time :", time.time() - a

    
    # print "Database version : %s " % ver
    
# except mdb.Error, e:
#     print "Error %d: %s" % (e.args[0],e.args[1])
#     sys.exit(1)
    
# finally:     
#     if connect:    
#         connect.close()

# with connect:
    
#     cur = connect.cursor()

#     cur.execute("Truncate table bandwidth")

#     a = time.time()
#     for i in range(20):
#         cur.execute("INSERT INTO bandwidth(global, local, incoming, outcoming) VALUES ("+rand()+","+rand()+","+rand()+","+rand()+")")
#         time.sleep(1)
#     print "time :", time.time() - a

"""
Client system sniffer

Use MySQLdb

@author: Olivier BLIN
"""


import MySQLdb as mdb
import sys
import time
import random


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


    def connection(self):
        while (not self.connect) and  (self.nbrtry < self.maxtry):
            self.nbrtry += 1
            try:
                self.connect = mdb.connect(
                    host=self.host, 
                    port=self.port,
                    user=self.user, 
                    passwd=self.passwd, 
                    db=self.database)
            except mdb.Error, e:
                print "Try %i - MySQLdb Error %d: %s" % (self.nbrtry, e.args[0],e.args[1])
            finally:
                if self.connect:
                    # print "MySQLdb connection OK" 
                    self.nbrtry = 0



    def execute(self, data):
        if self.connect:
            try:
                with self.connect:
                    cur = self.connect.cursor()
                    cur.execute(data)
            except mdb.Error, e:
                print "MySQLdb Error %d: %s" % (e.args[0],e.args[1])
        

    def close(self):
        if self.connect:
            self.connect.close
            # print "MySQLdb close" 



def rand():
    return str(random.randrange(0, 10000, 100))

import datetime

c = MySQLdata("192.168.1.144", "ndop", "ndop", "NDOP")
c.connection()

c.execute("Truncate table bandwidth")

nb = 100
it = datetime.datetime.now()
it -= datetime.timedelta(minutes=(30*nb))

a = time.time()
for i in range(nb):
    it += datetime.timedelta(minutes=30)
    vvv = it.strftime("%Y-%m-%d %H:%M:%S")

    req = "INSERT INTO bandwidth(date, global, local, incoming, outcoming) VALUES (\""+vvv+"\","+rand()+","+rand()+","+rand()+","+rand()+")"
    c.execute(req)
print "time :", time.time() - a

c.close()


#####################################

# c = MySQLdata("192.168.1.144", "ndop", "ndop", "NDOP")
# c.connection()

# a = time.time()

# req = "INSERT INTO bandwidth(global, local, incoming, outcoming) VALUES ("+rand()+","+rand()+","+rand()+","+rand()+")"
# c.execute(req)

# print "time :", time.time() - a

# c.close()
