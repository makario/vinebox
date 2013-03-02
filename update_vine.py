#!/bin/sh
cd /home/pi/vine
if ps -ef | grep -v grep | grep vine.py ; then #if already running
	exit 0
else
	python vine.py
	exit 0
fi
