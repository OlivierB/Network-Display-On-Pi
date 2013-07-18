=====================
Network Display On Pi
=====================

Network Display On Pi (NDOP) provide you a way to capture network
packets and send stats by websockets. Packets analysis is done through
differents modules you can choose.
NDOP main commands :

    help and commands list: ``ndop -h`` or ``ndop --help``

    run in consol: ``ndop``

    start ndop daemon: ``ndop --daemon``


see https://github.com/OlivierB/Network-Display-On-Pi.git


Files
=====

Files list:

* clean.sh: clean ndop directory (.pyc and setup install)

* launch_ndop.sh: start ndop without installation
  This script forward parameters to ndop

* setup.py: program installer (see next section)

* uninstall.sh: program uninstaller


Program management
==================

Install
-------

1. Check dependances

2. run ``python setup.py install``

Uninstall
---------

Just need to run ``./uninstall.sh``


