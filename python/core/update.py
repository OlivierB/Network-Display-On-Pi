#encoding: utf-8

"""
System Information collector

Optimization of websocket send

@author: Olivier BLIN
"""

import core.sniffer, core.wsserver, core.monitoring

WSSUBPROT_SYSDATA		= 'server_stat'
WSSUBPROT_BANDWIDTH 	= 'bandwidth'
WSSUBPROT_IPLIST 		= 'iplist'


class Update():
	def __init__(self, monnitor, pcap):
		self.m = monnitor
		self.p = pcap
		self.cl = core.wsserver.ClientsList()

		# values save

	def update(self):
		self.__update_sysdata()
		self.__update_bandwidth()
		self.__update_iplist()

	def __update_sysdata(self):
		self.cl.send(WSSUBPROT_SYSDATA, self.m.getState())

	def __update_bandwidth(self):
		self.cl.send(WSSUBPROT_BANDWIDTH, self.m.getState())

	def __update_iplist(self):
		self.cl.send(WSSUBPROT_IPLIST, self.m.getState())

