#!/bin/bash

bn=`basename $PWD`
if [ "$bn" == "scripts" ]; then
    cd ..
    bn=`basename $PWD`
    if [ "$bn" != "ndop" ]; then
        exit 1
    fi
fi


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
    if [ -d "/etc/init.d/" ]; then
        echo "service : /etc/init.d/ndop"
        cp ./scripts/service_ndop.sh /etc/init.d/ndop
        update-rc.d ndop defaults
    fi

    if ! [ -r "/etc/ndop/server_conf.json" ]; then
        mkdir -p /etc/ndop/
        ./ndop/config/conf_generator.py -oe > /etc/ndop/server_conf.json
        echo "Add server config file in /etc/ndop/"
    fi

fi