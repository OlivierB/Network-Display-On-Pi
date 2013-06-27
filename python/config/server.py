#encoding: utf-8

"""
Server configuration

@author: Olivier BLIN
"""

########################################
# Network information

# Websocket communication port
websocket_port = 9000

# listening device for sniffing
sniffer_device = "eth1"

# Net address of device
sniffer_device_net = "192.168.1.0"

# Mask address of device
sniffer_device_mask = "255.255.255.0"


########################################
# Modules selection
modules_list = ["netmod_top", "netmod_iplist", "netmod_loccomm", "netmod_protocols", "netmod_bandwidth", "netmod_dns"]
# module_list = ["netmod_classip"]


########################################
# Daemon parameters

# directories modifications
daemon_root_dir = "/"
daemon_working_dir = "/home/student/Documents/Network-Display-On-Pi/python"

# input, output and error file
daemon_stdin 	= '/dev/null'
daemon_stdout 	= '/tmp/out'
daemon_stderr 	= '/tmp/err'

# PID file
daemon_pid_file = '/var/run/ndop.pid'


########################################
# SQL Database connection

# Disabled SQL Database
db_sql_on	= True

db_host 	= "192.168.1.144"
db_user 	= "ndop"
db_passwd	= "ndop"
db_database	= "NDOP"
db_port 	= 3306


