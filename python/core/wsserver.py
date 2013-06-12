#encoding: utf-8

import threading
import time, types

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web




class WSHandler_main(tornado.websocket.WebSocketHandler):
    def open(self):
        print 'new connection'

    def on_message(self, message):
        print 'message received %s' % message

    def on_close(self):
        print 'connection closed'
        cl = ClientsList()
        cl.delClient(self)

    def select_subprotocol(self, subprotocols):
        cl = ClientsList()
        cl.addClient(self, subprotocols)
        return None
 

application = tornado.web.Application([
    (r'/', WSHandler_main)
])



class WsServer(threading.Thread):
    """
    
    """

    def __init__(self, port=9000):
        threading.Thread.__init__(self)

        # other
        self.port = port


        # HTTP server
        self.http_server = tornado.httpserver.HTTPServer(application)
        self.http_server.listen(9000)


    def run(self):

        print "WsServer : Server start..."

        try:

            tornado.ioloop.IOLoop.instance().start()


        except Exception as e:
            print "WsServer : ", e


    def stop(self):
        print 'WsServer : Server stop...'
        tornado.ioloop.IOLoop.instance().stop()



class ClientsList(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ClientsList, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    cli_list = dict()

    def __init__(self):
    # connection list
        pass

    def addClient(self, client, subprotocols):
        if len(subprotocols) > 0:
            for prot in subprotocols:
                print self.cli_list
                if prot in self.cli_list.keys():
                    self.cli_list[prot] += [client]
                else:
                    self.cli_list[prot] = [client]
                    print "add protocol : ", prot

    def delClient(self, client):
        for k in self.cli_list.keys():
            self.cli_list[k].remove(client)

    def send(self, proto, data):
        if proto == None:
            for p in self.cli_list.keys():
                for c in self.cli_list[p]:
                    c.write_message(data)
        elif isinstance(type(proto), types.StringType):
            if proto in self.cli_list.keys():
                for c in self.cli_list[proto]:
                    c.write_message(data)
        else:
            for p in proto:
                if p in self.cli_list.keys():
                    for c in self.cli_list[p]:
                        c.write_message(data)

    def listProto(self):
        return self.cli_list.keys()

    def getData(self):
        print self.cli_list

if __name__ == "__main__":

    ws = WsServer()
    ws.start()
    try:
        while 1:
            time.sleep(1)
    except KeyboardInterrupt:
        ws.stop()

    # http_server = tornado.httpserver.HTTPServer(application)
    # http_server.listen(9000)
    # tornado.ioloop.IOLoop.instance().start()