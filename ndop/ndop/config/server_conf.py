#encoding: utf-8

"""
Server configuration

@author: Olivier BLIN
"""

########################################
# Program information
__program__ = "NDOP"
__version__ = "0.0.3"
__description__ = "Network Sniffer with web display"


########################################
# Network information

# Websocket communication port
websocket_port = 9000

# listening device for sniffing
sniffer_device = "eth1"


########################################
# Modules selection
modules_list = [
    # ["netmod_http"],
    [
        "netmod_top", 
        "netmod_iplist", 
        "netmod_loccomm",
        "netmod_protocols",
        "netmod_dns",
        "netmod_pktstats",
        "netmod_bandwidth",
        "netmod_http"
    ]
]
# module_list = ["netmod_classip"]


########################################
# Daemon parameters

# input, output and error file
daemon_stdout = '/dev/null'
daemon_stderr = '/dev/null'

# PID file
daemon_pid_file = '/var/run/ndop.pid'

# Log file
log_file = "/var/log/ndoplog"


########################################
# SQL Database connection

# Disabled SQL Database
sql_on = True

sql_conf = {
    "host": "192.168.1.144",
    "user": "ndop",
    "passwd": "ndop",
    "database": "NDOP",
    "port": 3306,
}

