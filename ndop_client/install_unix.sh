#!/bin/bash

if [ $(id -u) -ne 0 ]; then
    echo -e "* ERROR: User $(whoami) is not root, and does not have sudo privileges"
    exit 1
fi

if [ ! -f "setup.py" ]; then
    echo -e "* ERROR: Setup file doesn't exist"
    exit 1
fi



python setup.py install

val="$?"
if [ "$val" == "0" ]; then
    ./clean.sh

fi