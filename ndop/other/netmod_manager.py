#encoding: utf-8

"""
Network modules manager

@author: Olivier BLIN
"""

import importlib

import core.wsserver


class NetmodManager():
    """
    Network modules manager
    Singleton
    """

    # Singleton creation
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(NetmodManager, cls).__new__(
                                cls, *args, **kwargs)
        return cls.__instance


    l_modules = list()

    def __init__(self, lmod=list()):
        if len(lmod) > 0:
            self.load_mod(lmod)

    # def add_mod()
    def get_mod(self):
        return self.l_modules

    def send(self, data):
        for nm in self.l_modules:
            nm[2].pkt_put(data)

    def stop(self):
         for nm in self.l_modules:
            nm[2].stop()

    def load_mod(self, lmod):
        """
        Load and start modules
        """
        # Singeton Webserver data (for websocket)
        wsdata = core.wsserver.ClientsList()

        for m in lmod:
            try:
                # import module
                module = importlib.import_module("modules." + m)

                # Check module main class
                getattr(module, "MyMod")

                # Create an instance
                modclass = module.MyMod(websocket=wsdata)
                # start module
                modclass.start()

                # add module to the list
                self.l_modules.append((m, module, modclass))
                print "Start module", m

                # except ImportError as e:
                #     print m, ":", e
                # except AttributeError as e:
                #     print m, ":", e
            except Exception as e:
                print m, ":", e

        return self.l_modules



if __name__ == "__main__":
    nm = NetmodManager(["A"])
    print nm.get_mod()

    nm2 = NetmodManager(["B"])
    print nm2.get_mod()

    nm3 = NetmodManager()
    print nm3.get_mod()