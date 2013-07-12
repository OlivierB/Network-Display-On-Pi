#!/usr/bin/env python
# -*- coding: utf-8 -*-

import websocket
import time
import pprint
import sys
import base64
import json



INDENT=2
ADDR="127.0.0.1:9001"

def get_list(addr):
    ws = websocket.create_connection("ws://" + addr + "/admin")
    ws.send("")
    pp = pprint.PrettyPrinter(indent=INDENT)
    result = json.loads(base64.b64decode(ws.recv()))
    # print "Protocols list :"
    pp.pprint(result)
    ws.close()



# --------------------------------
# main function and loop
def main():
    pp = pprint.PrettyPrinter(indent=INDENT)

    val = list()
    val.append("Sec-WebSocket-Protocol:bandwidth")

    try:
        ws = websocket.create_connection("ws://" + ADDR + "/", header=val)
    except:
        print "Connect error"
        return 0


    ws.send("")
    

    result = ""
    try:
        # result = json.loads(base64.b64decode(ws.recv()))
        result = json.loads(ws.recv())
        pp.pprint(result)
    except:
        print "decode error"
        print result

    # print "Protocols list :"
    
    ws.close()


    return 0

if __name__ == "__main__":
    sys.exit(main())
