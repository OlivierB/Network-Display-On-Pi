#!/bin/bash
res=`find . -name *.pyc`
if ! [ -z "$res" ]; then
	rm $res
	echo "Clean done"
else
	echo "Nothing to clean"
fi
