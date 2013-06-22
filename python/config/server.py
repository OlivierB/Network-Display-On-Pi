#encoding: utf-8

"""
Server configuration

@author: Olivier BLIN
"""

# Websocket communication port
websocket_port = 9000

# listening device for sniffing
sniffer_device = "eth1"

# Net address of device
sniffer_device_net = "192.168.1.0"

# Mask address of device
sniffer_device_mask = "255.255.255.0"

# Network module to launch with server
#module_list = ["netmod_classip"]
module_list = ["netmod_bandwidth", "netmod_top", "netmod_iplist", "netmod_loccomm", "netmod_protocols"]

