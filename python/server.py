#encoding: utf-8

"""
Network Display On Pi
NDOP

@author: Olivier BLIN
"""

# Python lib import
import sys, os, time
import argparse
import importlib
import datetime
import logging
import logging.handlers

# Project configuration file
import config.server as config

# Project import file
import core.sniffer, core.wsserver
import core.daemon as daemon


__program__ = "NDOP"
__version__ = "0.2.0"
__description__ = "Network Sniffer with web display"


class ServerArgumentParser(argparse.ArgumentParser):
    """
    Argument Parser
    """
    def __init__(self):
        super(ServerArgumentParser, self).__init__()
        
        # init
        self.description = "%s Version %s" % (__description__, __version__)
        
        # daemon server command. 'run' to avoid daemon mode
        self.add_argument(choices=['start', 'stop', 'restart', 'status', 'run'], dest='daemon_cmd',
            help="Daemon commands control (use 'run' for consol mode)" )

        self.add_argument("-p", "--port", default=config.websocket_port, type=int, dest="websocket_port", 
            help="Websocket server port (default: %i)" % config.websocket_port)

        self.add_argument("-i", "--interface", default=config.sniffer_device, dest="sniffer_device", 
            help="Network device for sniffing (default: %s)" % config.sniffer_device)

        self.add_argument("-m", "--mask", default=config.sniffer_device_mask, dest="sniffer_mask", 
            help="Local network mask (default: %s)" % config.sniffer_device_mask)

        self.add_argument("-n", "--net", default=config.sniffer_device_net, dest="sniffer_net", 
            help="Local network address (default: %s)" % config.sniffer_device_net)



class ServeurNDOP(daemon.Daemon):
    """
    Main class for NDOP server

    Add demonize function
    """

    def __init__(self, args):
        daemon.Daemon.__init__(self,
            config.daemon_pid_file,
            stdin=config.daemon_stdin,
            stdout=config.daemon_stdout,
            stderr=config.daemon_stderr,
            root_dir=config.daemon_root_dir,
            working_dir=config.daemon_working_dir)

        self.args = args

    def run(self):
        """
        Main server function

        Stand by Loop
        """

        # Get logger
        logger = logging.getLogger()

        logger.info(">>>>>>>>>>>>>>>>>>>> Network Sniffer with web display")
        logger.info("# " + datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))

        # Init websocket server (tornado)
        ws = core.wsserver.WsServer(self.args.websocket_port)
        # Init websocket data
        wsdata = core.wsserver.ClientsList()
        add_mod_prot(wsdata, config.modules_list)

        # init packet capture system
        sniff = core.sniffer.Sniffer(dev=self.args.sniffer_device)

        # Start services
        try:
            ws.start()
            time.sleep(0.5)
        except:
            ws.stop()
            exit(2)

        try:
            sniff.start()
            time.sleep(0.5)
        except:
            ws.stop()
            sniff.stop()
            exit(2)


        # Loop
        try:
            while 1:
                recv = sniff.get_data()
                for r in recv:
                    wsdata.send(r[0], r[1])

        except KeyboardInterrupt:
            logger.info("Stopping...")
        finally:
            # Sniffer stop
            sniff.stop()
            sniff.join()
            # Webserver stop
            ws.stop()
            ws.join()
            logger.info("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
                
        exit(0)


def add_mod_prot(wsdata, lmod):
    """
    Load modules to get protocols list
    """

    if len(lmod) > 0:
        for m in lmod:
            try:
                # import module
                module = importlib.import_module("modules." + m)

                # Check module main class
                getattr(module, "NetModChild")

                # Create an instance
                modclass = module.NetModChild()
                # Add protocol for the webserver
                wsdata.addProtocol(modclass.protocol)

            except:
                pass


def conf_logger(consol=False, debug=False):

    # create a file handler
    file_handler = logging.handlers.RotatingFileHandler(config.log_file,'a', 1000000)
    # output handler
    stdout_handler = logging.StreamHandler(sys.stdout)

    # create a logging format
    file_formatter = logging.Formatter('[%(levelname)s] : %(asctime)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    stdout_formatter = logging.Formatter('[%(levelname)s] -> %(message)s')
    stdout_handler.setFormatter(stdout_formatter)

    # Get logger
    logger = logging.getLogger()


    if debug:
        mod = logging.DEBUG
    else:
        mod = logging.INFO

    #  Set mode
    logger.setLevel(mod)
    file_handler.setLevel(mod)
    stdout_handler.setLevel(mod)


    # add the handlers to the logger
    logger.addHandler(file_handler)
    if consol:
        logger.addHandler(stdout_handler)


def main():
    """
    main function

    Command reader and ask root
    """

    # Get command line arguments
    args = ServerArgumentParser().parse_args()
    
    # Configure logger
    conf_logger('run' == args.daemon_cmd)
    # Get logger
    logger = logging.getLogger()

    # Be root to access network device
    if os.getuid() != 0:
        logger.warning("Can't start NDOP, need to be root !")
        exit(2)


    # Get daemon class
    daemon = ServeurNDOP(args)
    

    if 'start' == args.daemon_cmd:
        daemon.start()
    elif 'stop' == args.daemon_cmd:
        daemon.stop()
    elif 'restart' == args.daemon_cmd:
        daemon.restart()
    elif 'run' == args.daemon_cmd:
        daemon.run()

    sys.exit(0)




if __name__ == "__main__":
    sys.exit(main())