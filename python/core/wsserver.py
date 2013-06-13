#encoding: utf-8

import threading, multiprocessing
import time, types

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web




class WSHandler_main(tornado.websocket.WebSocketHandler):
    def open(self):
        # print '+++connection'
        pass

    def on_message(self, message):
        # print 'message received %s' % message
        pass

    def on_close(self):
        # print '---connection'
        cl = ClientsList()
        cl.delClient(self)

    def select_subprotocol(self, subprotocols):
        cl = ClientsList()
        return cl.addClient(self, subprotocols)
 

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
        self.http_server.listen(port)


    def run(self):

        print "WsServer : Server start..."

        try:

            tornado.ioloop.IOLoop.instance().start()


        except Exception as e:
            # print "WsServer : ", e
            tornado.ioloop.IOLoop.instance().stop()
            raise


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
    mutex = threading.Lock()

    def __init__(self):
    # connection list
        pass

    def addClient(self, client, subprotocols):
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
        self.mutex.acquire()
        for k in self.cli_list.keys():
            if client in self.cli_list[k]:
                self.cli_list[k].remove(client)
        self.mutex.release()


    def __send(self, client, data):
        try:
            client.write_message(data)
            
        except IOError:
            print "Send IOError"
        except Exception as e:
            print "WsServer Error : ", e

        return


    def send(self, proto, data):
        self.mutex.acquire()
        if proto == None:
            for p in self.cli_list.keys():
                for c in self.cli_list[p]:
                    self.__send(c, data)
            
        elif isinstance(type(proto), types.StringType):
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