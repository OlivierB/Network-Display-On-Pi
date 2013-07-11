#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python lib import
import os
import sys
import json
import argparse
import socket
import importlib
import logging
import logging.handlers
from pcap import findalldevs

# Project configuration file
from ndop.config import server_conf

UNIX_CONF_FILE = "/etc/ndop/server.cfg"

class ConfigChecker():

    """
    Singleton server config class

    Check all basic program configuration
    """

    # Singleton creation
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConfigChecker, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def config_checker(self):
        """
        Main checker function

        organize verifications according to launch mode
        """
        # Get command line arguments
        args = self.parser().parse_args()

        # required
        self.cmd = "run"
        self.daemon = args.daemon
        self.debug = args.debug

        # logger
        logger = logging.getLogger()

        # Only check config
        if args.test:
            conf_logger(debug=True, p_file=None)
            self.load_config("ndop.config.server_conf")
            logger.debug("%s : Load default config : OK" % self.__class__.__name__)
            self.try_config_override(UNIX_CONF_FILE)
            self.check_network(args)
            logger.debug("%s : Check network : OK" % self.__class__.__name__)
            self.check_sql(args, full=True)
            logger.debug("%s : Check SQL : OK" % self.__class__.__name__)
            self.check_modules(args)
            logger.debug("%s : Check modules : OK" % self.__class__.__name__)
            self.check_daemon_files(args)
            logger.debug("%s : Check Daemon files : OK" % self.__class__.__name__)
            self.check_pidfile(args)
            logger.debug("%s : Check PID file : OK" % self.__class__.__name__)
            self.check_logfile(args, daemon=True)
            logger.debug("%s : Check LOG file : OK" % self.__class__.__name__)

            logger.debug("%s : OK" % self.__class__.__name__)
            self.cmd = "test"
            return


        # Check user
        if not args.unroot and not self.is_root():
            raise UserMode("Need to be root or add -u (--unroot) argument !")
            return False

        # Load config file
        self.load_config("ndop.config.server_conf")

        # Check
        self.check_network(args)
        self.check_sql(args)
        self.check_modules(args)

        if self.daemon:
            self.check_daemon_files(args)
            self.check_pidfile(args)
            self.cmd = "daemon"

        self.check_logfile(args, daemon=self.daemon)
        conf_logger(debug=self.debug, p_file=self.log_file)

    def parser(self):
        """
        Create parser class to check input arguments
        """
        parser = argparse.ArgumentParser()
        # init
        parser.description = "%s Version %s" % (server_conf.__description__, server_conf. __version__)

        parser.add_argument("-d", "--debug", action='store_true', help="pass in debug mode")
        parser.add_argument("-u", "--unroot", action='store_true', help="authorize to launch ndop without root")
        parser.add_argument("-p", "--port", type=int, help="websocket server port")
        parser.add_argument("-i", "--interface", help="sniffer device")
        parser.add_argument("--daemon", action='store_true', help="daemon mode")
        parser.add_argument("--init", action='store_true', help="Module database initialisation")
        parser.add_argument("--reset", action='store_true', help="Module database reset")
        parser.add_argument("--test", action='store_true', help="Check configuration without start ndop")
        parser.add_argument('--version', action='version', version=('NDOP %s' % server_conf. __version__))
        return parser

    def get_elem(self, elem):
        """
        Get config file element

        raise ArgumentMissing exception if error
        """
        try:
            return getattr(self.file_conf, elem)
        except:
            raise ArgumentMissing("Cannot get \"%s\" element" % elem)

    def load_config(self, path):
        """
        Load a configuration file in python
        """
        try:
            # import module
            self.file_conf = importlib.import_module(path)

        except ImportError:
            raise ConfigFile("No config file")
        except Exception as e:
            raise ConfigFile("Error in %s :%s" % (path, e))

    def try_config_override(self, path):
        self.override_conf = None

        logger = logging.getLogger()
        logger.debug("%s : Try to override default config (%s)" % (self.__class__.__name__, path))
        try:
            error = "No file"
            f = open(os.getcwd()+"/ndop/config/server_conf.json", "r")
            with f:
                error = "Cannot read file"
                textconf = ""
                # Clean comments
                for line in f:
                    if line.find("//") == -1:
                        textconf += line
                error = "Cannot load JSON"
                loadconf = json.loads(textconf)
                error = "Argument error"
                self.override_conf = dict()
                for elem in loadconf:
                    if elem in dir(self.file_conf):
                        self.override_conf[elem] = loadconf[elem]
                        logger.debug("Override default config \"%s\"" % (elem))
                    else:
                        logger.debug("Override default config Error : \"%s\" is not in default config" % (elem))
        except:
            logger.debug("Override default config (%s) FAIL : %s" % (path, error))

    def check_sql(self, args, full=False):
        """
        Check SQL varibles
        """
        self.sql_on = self.get_elem("sql_on")
        if self.sql_on or full:
            self.sql_conf = self.get_elem("sql_conf")
            for elem in ["host", "user", "passwd", "database", "port"]:
                if not elem in self.sql_conf.keys():
                    raise ArgumentError("sql_conf : missing %s argument" % elem)
        else:
            self.sql_conf = dict()
            for elem in ["host", "user", "passwd", "database", "port"]:
                self.sql_conf[elem] = ""

    def check_network(self, args):
        """
        Check network variables
        """
        # Get websocket port
        if args.port is None:
            self.ws_port = self.get_elem("websocket_port")
        else:
            self.ws_port = args.port
        # Check ws port
        if self.ws_port < 1024:
            raise ArgumentConfigError("Cannot use system port")
        # Check listen port
        if self.is_port_open(self.ws_port):
            raise ArgumentConfigError("Port %i already in use" % self.ws_port)

        # Get sniffer device
        if args.interface is None:
            self.sniff_dev = self.get_elem("sniffer_device")
        else:
            self.sniff_dev = args.interface
        # Check sniff device
        if not self.sniff_dev in self.all_netdevs():
            raise ArgumentConfigError("No \"%s\" network device" % self.sniff_dev)
            return False

    def check_daemon_files(self, args):
        self.daemon_stdout = self.get_elem("daemon_stdout")
        if not self.is_file_writable(self.daemon_stdout):
            raise ArgumentConfigError("stdout : Cannot write in %s" % self.daemon_stdout)

        self.daemon_stderr = self.get_elem("daemon_stderr")
        if not self.is_file_writable(self.daemon_stderr):
            raise ArgumentConfigError("stderr : Cannot write in %s" % self.daemon_stderr)

    def check_pidfile(self, args):
        self.daemon_pid_file = self.get_elem("daemon_pid_file")
        if not self.is_file_writable(self.daemon_pid_file):
            raise ArgumentConfigError("pid file : Cannot write in %s" % self.daemon_pid_file)

    def check_logfile(self, args, daemon=False):
        if daemon:
            self.log_file = self.get_elem("log_file")
            if not self.is_file_writable(self.log_file):
                    raise ArgumentConfigError("log file : Cannot write in %s" % self.log_file)
        else:
            self.log_file = None

    def check_modules(self, args):
        """
        Check and load modules class

        Create protocols list for websocket server
        """
        ll_mod = self.get_elem("modules_list")
        self.ll_modules = list()
        self.l_protocols = list()

        if len(ll_mod) > 0:
            for l_mod in ll_mod:
                if not type(l_mod) is list:
                    raise ArgumentError("Bad modules declaration")

                l_modules = list()
                for mod in l_mod:
                    try:
                        # import module
                        module = importlib.import_module("ndop.modules." + mod)

                        # Check module main class
                        getattr(module, "NetModChild")

                        # Create an instance
                        modclass = module.NetModChild()

                        # Add protocol and module
                        l_modules.append(modclass)
                        self.l_protocols.append(modclass.protocol)
                    except Exception as e:
                        raise ArgumentConfigError("Module %s : Cannot be loaded : %s" % (mod, e))

                if len(l_modules) > 0:
                    self.ll_modules.append(l_modules)

    def is_root(self):
        if os.getuid() != 0:
            return False
        else:
            return True

    def is_file_writable(self, path):
        """
        Check if it is possible to write in the given file
        """
        if os.path.exists(path):
            if os.access(path, os.W_OK):
                return True
            else:
                return False
        else:
            try:
                with open(path, "a+"):
                    pass
                os.remove(path)
                return True
            except IOError:
                pass
            return False

    def is_port_open(self, port):
        """
        Check if asked websocket port is available
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('', port))
        sock.close()
        if result == 0:
            return True
        else:
            return False

    def all_netdevs(self):
        """
        list all available network devices

        need to be root or have special authorisation
        """
        l = list()
        for d in findalldevs():
            l.append(d[0])
        return l


def conf_logger(debug=False, p_file=None):
    """
    Configure general logger parameters
    """
    # Set debug mode or not
    if debug:
        mod = logging.DEBUG
    else:
        mod = logging.INFO

    # Get logger
    logger = logging.getLogger()
    logger.setLevel(mod)

    if p_file is not None:
        # Log in a file
        file_handler = logging.handlers.RotatingFileHandler(p_file, 'a', 1000000)
        file_formatter = logging.Formatter('[%(levelname)s] : %(asctime)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(mod)
        logger.addHandler(file_handler)

    else:
        # output handler
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_formatter = logging.Formatter('[%(levelname)s] -> %(message)s')
        stdout_handler.setFormatter(stdout_formatter)
        stdout_handler.setLevel(mod)
        logger.addHandler(stdout_handler)


class ConfigCenter(Exception):

    """ndop config error"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.__class__.__name__ + " : " + repr(self.value)


class ArgumentMissing(ConfigCenter):

    """Argument missing in the file"""
    pass


class ArgumentError(ConfigCenter):

    """
    Argument is present but wrong informed

    Example : type or structure error
    """
    pass


class ConfigFile(ConfigCenter):

    """Config file import error"""
    pass


class ArgumentConfigError(ConfigCenter):

    """Argument has a wrong value"""
    pass


class UserMode(ConfigCenter):

    """User cannot run the program"""
    pass
