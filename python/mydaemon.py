#!/usr/bin/env python

import sys, time, os, argparse
from core.daemon import Daemon
import config.server

class MyDaemon(Daemon):
    # def __init__(self):
        # Daemon.__init__(self, '/tmp/daemon-example.pid', stdout='/tmp/out', stderr='/tmp/err')

    def run(self):
        try:    
            while True:
                time.sleep(1)
                print "eeee"
                # sys.stdout.write("HELLO\n")
        except:
            pass

class ServerArgumentParser(argparse.ArgumentParser):
    """
    Argument Parser
    """
    
    def __init__(self):
        super(ServerArgumentParser, self).__init__()
        
        # init
        self.description = "%s Version %s" % ("__description__", "__version__")
        
        self.add_argument(choices=['start', 'stop', 'restart', 'run'], dest='daemon_cmd',
            help="Daemon control command" )


        # self.add_argument('daemon_cmd', nargs="?", 
        #     help="Daemon command")

        self.add_argument("-p", "--port", default=config.server.websocket_port, type=int, dest="websocket_port", 
            help="Websocket server port (default: %i)" % config.server.websocket_port)

        self.add_argument("-i", "--interface", default=config.server.sniffer_device, dest="sniffer_device", 
            help="Network device for sniffing (default: %s)" % config.server.sniffer_device)

        self.add_argument("-m", "--mask", default=config.server.sniffer_device_mask, dest="sniffer_mask", 
            help="Local network mask (default: %s)" % config.server.sniffer_device_mask)

        self.add_argument("-n", "--net", default=config.server.sniffer_device_net, dest="sniffer_net", 
            help="Local network address (default: %s)" % config.server.sniffer_device_net)


if __name__ == "__main__":
    daemon = MyDaemon('/tmp/daemon-example.pid', stdout='./out', stderr='/tmp/err')

    args = ServerArgumentParser().parse_args()
    
    if 'start' == args.daemon_cmd:
        daemon.start()
    elif 'stop' == args.daemon_cmd:
        daemon.stop()
    elif 'restart' == args.daemon_cmd:
        daemon.restart()
    elif 'run' == args.daemon_cmd:
        daemon.run()
    else:
        print "Unknown command"
        sys.exit(2)
    sys.exit(0)
