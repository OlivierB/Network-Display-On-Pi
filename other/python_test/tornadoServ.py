#encoding: utf-8

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
 

class WSHandler_main(tornado.websocket.WebSocketHandler):
    def open(self):
        print 'new connection'
        self.write_message("53")
        client = self

    def on_message(self, message):
        print 'message received %s' % message

    def on_close(self):
        print 'connection closed'

    def select_subprotocol(self, subprotocols):
        print subprotocols
        return None
 

application = tornado.web.Application([
    (r'/', WSHandler_main)
])


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(9000)
    tornado.ioloop.IOLoop.instance().start()