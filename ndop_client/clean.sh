#!/bin/bash

bn=`basename $PWD`
if [ "$bn" == "scripts" ]; then
    cd ..
    bn=`basename $PWD`
    if [ "$bn" != "ndop" ]; then
        exit 1
    fi
fi

res=`find . -name *.pyc`
if ! [ -z "$res" ]; then
    rm $res
    echo "Clean done : *.pyc"
fi

if [ -d build/ ] || [ -d dist/ ] || [ -d *egg-info/ ]; then
    rm -r build/ dist/ *egg-info  2> /dev/nul
    echo "Clean done : build files"
fi