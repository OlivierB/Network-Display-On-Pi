#!/bin/bash

bn=`basename $PWD`
if [ "$bn" == "scripts" ]; then
    cd ..
    bn=`basename $PWD`
    if [ "$bn" != "ndop" ]; then
        exit 1
    fi
fi

python -m ndop.server $@
exit 0
