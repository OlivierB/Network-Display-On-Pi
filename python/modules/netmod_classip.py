#encoding: utf-8

"""
Client system monitoring

inherit from NetModule

@author: Olivier BLIN
"""


import time

import netmodule as netmod

class NetModChild(netmod.NetModule):
    def __init__(self):
        netmod.NetModule.__init__(self, protocol='classip')




