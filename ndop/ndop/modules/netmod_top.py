# encoding: utf-8

"""
Client system monitoring

Use psutil

inherit from NetModule

@author: Olivier BLIN
"""

# Python lib import
import psutil

# Project file import
from netmodule import NetModule


class NetModChild(NetModule):
    """
    System load
    """

    def __init__(self, *args, **kwargs):
        NetModule.__init__(self, updatetime=1, protocol='server_stat', *args, **kwargs)

        if psutil.__version__ < '0.7.0':
            self.logger.warning("Update psutil to 0.7.1")

    def update(self):

        # get data
        val = dict()
        val["mem_load"] = psutil.virtual_memory()[2]
        val["swap_load"] = psutil.swap_memory()[3]
        val["proc_load"] = psutil.cpu_percent(interval=0)
        val["proc_load_perc"] = psutil.cpu_percent(interval=0, percpu=True)

        # send data
        return val
