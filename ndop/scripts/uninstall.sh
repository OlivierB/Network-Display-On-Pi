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



python setup.py install --record install.record

for i in $(cat install.record); do
    rm  $i
done

echo -e "\n\n* SUCCESS: Uninstall complete."
rm install.record

if [ -r "/etc/init.d/ndop" ]; then
    echo "remove service : /etc/init.d/ndop"
    rm /etc/init.d/ndop
    update-rc.d ndop remove
fi

if [ -r "/etc/ndop/server_conf.json" ]; then
    rm /etc/ndop/server_conf.json
    rmdir /etc/ndop
    echo "Delete server config file in /etc/ndop/"
fi
