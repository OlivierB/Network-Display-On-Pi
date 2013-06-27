#encoding: utf-8

"""
main module for monitoring

@author: Olivier BLIN
"""

# Python lib import
import time, datetime


class NetModule():
    """
    Module main class
    Define most usefull inheritance functions
    """
    def __init__(self, updatetime=10, savetime=('m', 30), protocol=None):

        # intern variable
        self.protocol       = protocol
        self.updatetime     = updatetime
        self.lastupdate     = 0

        self.save_timecode(savetime)
        self.save_timewait()


    def update(self):
        return None

    def pkt_handler(self, pkt):
        pass

    def get_protocol(self):
        return self.protocol

    def get_data(self):
        if (time.time() - self.lastupdate) > self.updatetime:
            self.lastupdate = time.time()
            return self.update()
        else:
            return None

    def get_sql(self):
        if time.time() - self.savetime > self.savewait:
            self.save_timewait()
            return self.save()
        else:
            return None

    def save_timewait(self):
        if self.savecode[0] == 'm':
            d = datetime.datetime.today()
            self.savetime = time.time()
            self.savewait = (self.savecode[1] - (d.minute % self.savecode[1]) ) * 60 - d.second
        elif self.savecode[0] == 'h':
            d = datetime.datetime.today()
            self.savetime = time.time()
            self.savewait = (self.savecode[1] - (d.hour % self.savecode[1]) ) * 3600 - (d.minute*60) - d.second
        else:
            self.savetime = time.time()
            self.savewait = 30*60
            print "NetModule : Time save error"


    def save_timecode(self, savetime):
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


    def reset(self):
        pass

    def save(self):
        pass
