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

import MySQLdb as mdb
import sys
import time
import random

connect = None

def rand():
    return str(random.randrange(0, 1000, 10))

# try:
connect = mdb.connect(
        host="192.168.1.144", 
        port=3306, 
        user="ndop", 
        passwd="ndop", 
        db="NDOP")



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

with connect:
    
    cur = connect.cursor()

    cur.execute("Truncate table bandwidth")

    a = time.time()
    for i in range(20):
        cur.execute("INSERT INTO bandwidth(global, local, incoming, outcoming) VALUES ("+rand()+","+rand()+","+rand()+","+rand()+")")
        time.sleep(1)
    print "time :", time.time() - a

