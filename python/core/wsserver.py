#encoding: utf-8

"""
Websocket module

Manage websocket connections and subprotocols
to send data to clients

Use python tornado webserver

@author: Olivier BLIN
"""


import threading, multiprocessing
import time, types
import logging

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web


class WSHandler_main(tornado.websocket.WebSocketHandler):
    """
    handler for main server page ("/")
    """
    def open(self):
        pass

    def on_message(self, message):
        pass

    def on_close(self):
        cl = ClientsList()
        cl.delClient(self)

    def select_subprotocol(self, subprotocols):
        """
        Subprotocol defined the type of connection

        If no protocol is given, the connection is closed
        """
        cl = ClientsList()
        prot = cl.addClient(self, subprotocols)
        if prot in cl.getProtocols():
            return prot
        else:
            self.close()
            return None
 

# associate handler function and page
application = tornado.web.Application([
    (r'/', WSHandler_main)
])


class WsServer(threading.Thread):
    """
    Thread class for tornado webserver
    """

    def __init__(self, port=9000):
        threading.Thread.__init__(self)

        # HTTP server
        self.http_server = tornado.httpserver.HTTPServer(application)
        self.http_server.listen(port)
        self.clientList = ClientsList()

        self.log = logging.getLogger()


    def run(self):
        self.log.info("WsServer : Server started...")
        try:
            tornado.ioloop.IOLoop.instance().start()
            self.log.info('WsServer : Server stopped...')
        except KeyboardInterrupt:
            self.log.info('WsServer : Server stopped on interruption signal...')
        except Exception as e:
            self.log.error("WsServer : ", exc_info=True)

    def stop(self):
        self.clientList.closeCom()
        tornado.ioloop.IOLoop.instance().stop()



class ClientsList(object):
    """
    Singleton class to collect client data
    """

    # Singleton creation
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ClientsList, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    #  class values
    cli_list = dict()
    protocols_list = list()
    mutex = threading.Lock()


    def addClient(self, client, subprotocols):
        """
        Add a websocket client only if it has a subprotocol
        """
        prot = None
        if len(subprotocols) > 0:
            # Select the first protocol
            prot = subprotocols[0]
            self.mutex.acquire()
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
        except Exception as e:
            pass


    def send(self, proto, data):
        """
        Send data to client
        proto = NoneType    -> Send to all protocols
        proto = StringType  -> Send to "StringType" protocol
        proto = StirngTyp list  -> Send to all protols in the list
        """
        self.mutex.acquire()
        if type(proto) is type(None):
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

    def listProto(self):
        return self.cli_list.keys()

    def getData(self):
        return self.cli_list


    def addProtocol(self, prot):
        if prot != None:
            self.protocols_list.append(prot)

    def getProtocols(self):
        return self.protocols_list


if __name__ == "__main__":

    ws = WsServer()
    ws.start()
    try:
        while 1:
            time.sleep(1)
    except KeyboardInterrupt:
        ws.stop()
