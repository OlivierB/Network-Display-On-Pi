#!/usr/bin/env python
# -*- coding: utf-8 -*-

import websocket
import argparse
import thread
import time
import pprint
import sys
import base64
import json

INDENT=2

__description__ = "NDOP client"
__version__ = "0.0.1"

DEF_ADDR = "127.0.0.1:9000"

def parser():
    """
    Create parser class to check input arguments
    """
    parser = argparse.ArgumentParser()
    # init
    parser.description = "%s Version %s" % (__description__,__version__)

    parser.add_argument("protocols", nargs='*', help="select some protocols")
    parser.add_argument("--addr", help="websocket server address", default=("%s" % DEF_ADDR))
    parser.add_argument("--list", action='store_true', help="Protocols list")
    parser.add_argument('--version', action='version', version=('NDOP %s' %  __version__))
    return parser

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


def get_list(addr):
    ws = websocket.create_connection("ws://"+addr+"/admin")
    ws.send("")
    pp = pprint.PrettyPrinter(indent=INDENT)
    result =  json.loads(base64.b64decode(ws.recv()))
    print "Protocols list :"
    pp.pprint(result)
    ws.close()


def main():
    p = ProtoMGMT()

    args = parser().parse_args()

    if args.list:
        try:
            get_list(args.addr)
        except:
            print "Cannot get list"
        return 0

    for a in args.protocols:
        p.add_proto(a)

    if len(p.l_proto) == 0:
        print "Listen ALL protocols"
    else:
        print "Listen :", p.l_proto

    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("ws://"+args.addr+"/admin",
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
    sys.exit(main())
    


