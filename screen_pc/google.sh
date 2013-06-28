#!/bin/bash
while [ $# -gt 0 ]; do
	google-chrome --kiosk --incognito --no-context-menu --enable-logging --log-level=0 http://$1 2> /dev/null 1> /dev/null &
	shift
done
