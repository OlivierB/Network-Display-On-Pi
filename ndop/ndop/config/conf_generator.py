#! /usr/bin/env python
# -*- coding: utf-8 -*-

import importlib
import json
import sys
import argparse


FILE_OUT = "./server_conf.json"

header = \
"""\
// Configuration file for ndop
// This file is writen in JSON syntax
// http://fr.wikipedia.org/wiki/JavaScript_Object_Notation
"""

ex_code = \
"""
{
////////////////////////////
    // tornado websocket port
    "websocket_port": 9005,

////////////////////////////
    // Ethernet interface for packets capture
    "sniffer_device": "eth0",

////////////////////////////
    // Modules list :
    // List of sniffer (different process)
    // and for each sniffer, a list of module

    // Do NOT use the same module two times
    //     they cannot be differenciate

    // Do NOT create more sniffer than processor core
    //     performance will decline

    "modules_list": [
        // SNIFFER 1 : modules list
        [
            "netmod_top",
            "netmod_iplist",
            "netmod_loccomm",
            "netmod_protocols",
            "netmod_dns",
            "netmod_pktstats",
            "netmod_bandwidth"
        ],

        // SNIFFER 2 : modules list
        [
            "netmod_http"
        ]
    ],

////////////////////////////
    // Daemon files

    "daemon_pid_file": "/var/run/ndop.pid",
    "daemon_log_file": "/var/log/ndoplog",

    // Output files standard and error
    "daemon_stdout": "/dev/null",
    "daemon_stderr": "/dev/null",

////////////////////////////
    // Database Config

    // Enable or disable database saving
    "db_on": false,

    // DB Type
    "db_class": "MySQL_database",

    // DB Config
    "db_conf": {
        "host": "127.0.0.1",
        "user": "ndop",
        "passwd": "ndop",
        "database": "NDOP",
        "port": 3306
    }
}
"""


def main():
    """
    main function
    """

    args = parser().parse_args()

    final = ""

    if (not args.noheader):
        final += header + "\n"

    if (args.gen):
        if (args.example):
            tmp = "//"
            tmp += ex_code.replace("\n", "\n// ")
            tmp += "\n\n"
            final += tmp


        conf = load_config("server_conf")
        # Construct dict with values
        res = dict()
        for elem in dir(conf):
            if elem[0:2] != "__":
                val = getattr(conf, elem)
                res[elem] = val

        # Try convert conf in JSON
        try:
            jsdumps = json.dumps(res, ensure_ascii=False, sort_keys=True, encoding="UTF-8",
                indent=4, separators=(',', ': '))
            final += jsdumps + "\n"
        except:
            sys.stderr.write("JSONize...FAIL\n")


    else:
        if (args.example):
            final += ex_code+"\n"


    
    if (args.stdout):
        if len(final) > 0:
            sys.stdout.write(final)
        else:
            sys.stderr.write("File empty\n")
    else:
        sys.stdout.write("JSONize...OK\nWrite in :%s\n" % FILE_OUT)
        f = open(FILE_OUT, "w+")
        with f:
            f.write(final)

def parser():
    """
    Create parser class to check input arguments
    """
    parser = argparse.ArgumentParser()
    # init
    parser.description = "Config generator"

    parser.add_argument("-o", "--stdout", action='store_true', help="write result in stdout")
    parser.add_argument("--noheader", action='store_true', help="do not write header information")
    parser.add_argument("-e", "--example", action='store_true', help="write config example")
    parser.add_argument("-g", "--gen", action='store_true', help="write generated config from server_conf.py")
    
    return parser

def load_config(path):
    """
    Load a configuration file in python
    """
    try:
        # import module
        file_conf = importlib.import_module(path)
        return file_conf
    except ImportError:
        raise ConfigFile("No config file")
    except Exception as e:
        raise ConfigFile("Error in%s :%s" % (path,e))


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


if __name__ == "__main__":
    sys.exit(main())
