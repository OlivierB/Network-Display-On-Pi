import websocket
import thread
import time
import pprint
import sys
import base64
import json

INDENT=2

def on_message(ws, message):
    pp = pprint.PrettyPrinter(indent=INDENT)
    message = json.loads(base64.b64decode(message))
    proto=message["proto"]
    data=message["data"]

    p = ProtoMGMT()


    if len(p.l_proto) == 0 or proto in p.l_proto:
        print "#####START"
        
        print "PROTO :", proto
        pp.pprint(data)
        print "END#######"

def on_error(ws, error):
    # print "Error :",error
    pass

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    def run(*args):
        while 1:
            time.sleep(1)
        ws.close()
        print "thread terminating..."
    thread.start_new_thread(run, ())

class ProtoMGMT(object):
    """
    Singleton class to collect client data
    """

    # Singleton creation
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ProtoMGMT, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    #  class values
    l_proto = list()

    def add_proto(self, proto):
        self.l_proto.append(proto)


def get_list():
    ws = websocket.create_connection("ws://192.168.1.137:9000/admin")
    ws.send("")
    pp = pprint.PrettyPrinter(indent=INDENT)
    result =  json.loads(base64.b64decode(ws.recv()))
    print "Protocols list :"
    pp.pprint(result)
    ws.close()


def main(*args):
    p = ProtoMGMT()

    if len(args) > 0:
        if args[0] == "--list":
            get_list()
            return 0

        for a in args:
            p.add_proto(a)
    if len(p.l_proto) == 0:
        print "Listen ALL protocols"
    else:
        print "Listen :", p.l_proto

    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("ws://192.168.1.137:9000/admin",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open

    try:
        ws.run_forever()
    except KeyboardInterrupt:
        print "Stopping..."
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
    


