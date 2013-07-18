Network-Display-On-Pi
=====================

Network Display On Pi (NDOP) is a network monitoring service which provides you a way to capture packets and send stats by websockets. Packets analysis is done through differents modules you can choose or create.

# Repository structure

* ndop : NDOP python server
	* scripts : short cut actions (bash scripts)
	* ndop : python files
* ndop_client : small python client for NDOP server
* www : web client for NDOP server


# NDOP server

## Requirements

* [pypcap 0.7.1](http://sourceforge.net/projects/pylibpcap/)
* [psutil 0.6.4](https://code.google.com/p/psutil/)
* python-tornado
* python-argparse


## Installation

Download the git repository or clone it:
```git clone https://github.com/OlivierB/Network-Display-On-Pi.git```

Go in the NDOP server repository :
```cd ndop```


*If you don't want to install NDOP in your system, you can try it with:*
``` ./script/launch_ndop.sh ```

There are two ways to install NDOP :
* basic install with setup.py
* complete install with the *installer* bash script **Only Linux users**
	* Add a config file in ```/etc/ndop/```
	* Add a service script (init.d)

**Do not forgot to run commands in superuser mode**

For a basic install :
```python setup.py install```

For a complete install :
``` ./scripts/install_unix.sh ```


## Uninstall

In superuser mode :
```
cd ndop
./script/uninstall.sh
```

*uninstall remove server config file and service script*

## Configuration

Configuration file is ```/etc/ndop/server_conf.json```
If the file doesn't exist, the only way you have to configure NDOP server is to change values in the config file of ndop package (```ndop/config/server_conf.py```). After make changes, you need to reinstall it or use the launch script (```./script/launch_ndop.sh```)


## Utilisation
* help : ```ndop -h```

* test config : ```ndop --test``` (tell you if server config works)
* run in console : ```ndop```
* daemon mode : ```ndop --daemon``` (or use service script ```service ndop start```)
* pass in debug mode with '-d' option


## Add a new module
create a new python file in ```ndop/modules``` with skeleton module :
* ```cd ndop/modules/```
* ```cp netmod_skeleton.py netmod_mymodule.py```
* Change protocol in ```__init___``` function



# python NDOP client

## Installation

* python-argparse
* [python-websocket](https://pypi.python.org/pypi/websocket-client/0.7.0)
* [python-curses](http://docs.python.org/2/howto/curses.html)


Installation Commands:
```
cd ndop_client
python setup.py install
```

You can also use bash install script:
```
./install_unix.sh
```

## Utilization

If your server is on the local computer, you just need to run :
```
cd ndop_client
python client
```
because default bind address is 127.0.0.1:9000.

otherwise, configure distant address correctly with ```--addr``` option
```
python client --addr ADDRESS:PORT
```

# Integrated web client
## Configure a basic monitoring computer

### Install :
- openbox
- google chrome
- unclutter (optional mouse hider)
- sakura (optional good and light terminal ;)

### openbox configuration :
* create file ~/.config/openbox/autostart
* write :
```
xset -dpms &
xset s noblank &
xset s off &
sakura &
~/google.sh ADDR
```

### google chrome script

Small script to launch google
```
#!/bin/bash
while [ $# -gt 0 ]; do
	google-chrome --kiosk --incognito --no-context-menu --enable-logging --log-level=0 http://$1 2> /dev/null 1> /dev/null &
	shift
done
```

If there is a problem, it could be interesting to see google-chrome logs :
```
tail -f ~/.config/google-chrome/chrome_debug.log
```
