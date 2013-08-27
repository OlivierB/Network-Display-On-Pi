# -*- coding: utf-8 -*-

"""
Websocket module

Manage websocket connections and subprotocols
to send data to clients

Use python tornado webserver

@author: Olivier BLIN
"""

# Python lib import
import logging
import base64
import json

from threading import Thread, Lock
from tornado import web, websocket, httpserver, ioloop, netutil, process
from time import sleep


class WSHandler_main(websocket.WebSocketHandler):

    """
    handler for main server page ("/") -> Websocket
    """
    def open(self):
        pass

    def on_message(self, message):
        pass

    def on_close(self):
        cl = WsData()
        cl.delClient(self)

    def select_subprotocol(self, subprotocols):
        """
        Subprotocol defined the type of connection

        If no protocol is given, the connection is closed
        """
        cl = WsData()
        prot = cl.addClient(self, subprotocols)
        if prot is not None:
            return prot
        else:
            # self.close()
            return None


class WSHandler_admin(websocket.WebSocketHandler):

    """
    handler for main server page ("/admin") -> Websocket
    """
    def open(self):
        try:
            cl = WsData()
            data = base64.b64encode(json.dumps(cl.getProtocols()))
            data = dict()
            data["l_protocols"] = cl.getProtocols()
            self.write_message(data)
        except Exception:
            logger = logging.getLogger()
            logger.debug("WsServer send : Can't send to admin")
        self.close()

    def on_message(self, message):
        pass

    def on_close(self):
        self.close()

    def select_subprotocol(self, subprotocols):
        pass


class WSHandler_online(web.RequestHandler):

    """
    handler for server page ("/online") -> HTTP
    """
    def get(self):
        self.write("ndop")
        # self.set_status(200)
        self.finish()


# associate handler function and page
application = web.Application([
    (r'/', WSHandler_main),
    (r'/online', WSHandler_online),
    (r'/admin', WSHandler_admin)
])


class WsServer(Thread):

    """
    Thread class for tornado webserver
    """

    def __init__(self, port):
        Thread.__init__(self)

        # HTTP server
        self.http_server = httpserver.HTTPServer(application)
        self.http_server.listen(port)
        self.clientList = WsData()

        self.log = logging.getLogger()
        self.port = port

    def run(self):

        self.log.info("WsServer : Server started on port %i" % self.port)
        try:
            ioloop.IOLoop.instance().start()
            self.log.info('WsServer : Server stopped...')
        except KeyboardInterrupt:
            self.log.info('WsServer : Server stopped on interruption signal...')
        except Exception as e:
            self.log.debug("WsServer :", exc_info=True)
            self.log.error("WsServer :", e)
        finally:

            ioloop.IOLoop.instance().close(all_fds=True)

    def stop(self):
        self.clientList.closeCom()
        ioloop.IOLoop.instance().stop()




class WsData(object):

    """
    Singleton class to collect websocket data

    clients management
    """

    # Singleton creation
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(WsData, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    #  class values
    cli_list = dict()
    protocols_list = list()
    mutex = Lock()

    def addClient(self, client, subprotocols):
        """
        Add a websocket client only if it has a subprotocol
        """

        prot = None
        for elem in subprotocols:
            if elem in self.protocols_list:
                prot = elem
                break

        self.mutex.acquire()
        if prot is not None:
            if prot in self.cli_list.keys():
                self.cli_list[prot] += [client]
            else:
                self.cli_list[prot] = [client]
        self.mutex.release()

        return prot

    def delClient(self, client):
        """
        Delete a websocket client from list
        """
        self.mutex.acquire()
        for k in self.cli_list.keys():
            if client in self.cli_list[k]:
                self.cli_list[k].remove(client)
        self.mutex.release()

    def closeCom(self):
        """
        Close all websockets
        """
        for k in self.cli_list.keys():
            for c in self.cli_list[k]:
                try:
                    c.close()
                    self.cli_list[k].remove(c)
                except:
                    pass

    def __send(self, client, data):
        """
        Send data to clients
        Exception managment
        """
        try:
            client.write_message(data)
        except Exception:
            logger = logging.getLogger()
            logger.debug("WsServer send : Can't send to client")

    def send(self, proto, data):
        """
        Send data to client
        proto = NoneType    -> Send to all protocols
        proto = StringType  -> Send to "StringType" protocol
        proto = StirngTyp list  -> Send to all protols in the list
        """
        self.mutex.acquire()
        if type(proto) is None:
            for p in self.cli_list.keys():
                for c in self.cli_list[p]:
                    self.__send(c, data)

        elif type(proto) is type(str()):
            if proto in self.cli_list.keys():
                for c in self.cli_list[proto]:
                    self.__send(c, data)

        else:
            for p in proto:
                if p in self.cli_list.keys():
                    for c in self.cli_list[p]:
                        self.__send(c, data)

        self.mutex.release()

    def addProtocol(self, prot):
        if prot is not None:
            self.protocols_list.append(prot)

    def addListProtocols(self, lprot):
        for prot in lprot:
            if prot is not None:
                self.protocols_list.append(prot)

    def getProtocols(self):
        return self.protocols_list
