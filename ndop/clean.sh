#!/bin/bash
res=`find . -name *.pyc`
if ! [ -z "$res" ]; then
	rm $res
	rm -r build/ dist/ *egg-info 
	echo "Clean done"
else
	echo "Nothing to clean"
fi
