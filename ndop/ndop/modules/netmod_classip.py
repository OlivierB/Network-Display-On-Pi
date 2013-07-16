# encoding: utf-8

"""
Client system monitoring

inherit from NetModule

@author: Olivier BLIN
"""

# Project file import
from netmodule import NetModule

class NetModChild(NetModule):

    def __init__(self, *args, **kwargs):
        NetModule.__init__(self, updatetime=5, savetime=('m', 1), protocol='classip', *args, **kwargs)
        self.last = None

    def update(self):
        return self.last

    def pkt_handler(self, pkt):
        if pkt.is_protocol("Ethernet", "IPv4"):
            self.last = dict()
            self.last["ip"] = pkt.Ether.payload.src

    def database_init(self, db_class):
        req = \
"""
CREATE TABLE IF NOT EXISTS `test_table` (
  `global` int(11) NOT NULL,
  `local` int(11) NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 ;
"""

        db_class.execute(req)

    def database_save(self, db_class):
        req = "INSERT INTO test_table(global, local) VALUES (10,5)"

        db_class.execute(req)
