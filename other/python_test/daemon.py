#! /usr/bin/env python
# -*- coding: utf-8 -*-

# http://stackoverflow.com/questions/473620/how-do-you-create-a-daemon-in-python
# http://www.gavinj.net/2012/06/building-python-daemon-process.html

import time
import daemon

import grp
import signal
import lockfile

RUN = True

def initial_program_setup():
	global RUN
	RUN = True

def do_main_program():
	while RUN:
		time.sleep(1)

def program_cleanup():
	global RUN
	RUN = False

def reload_program_config():
	pass


context = daemon.DaemonContext(
    umask=0o002,
    pidfile=lockfile.FileLock('/var/run/spam2.pid'),
    )

context.signal_map = {
    signal.SIGTERM: program_cleanup,
    signal.SIGINT: program_cleanup,
    signal.SIGHUP: 'terminate',
    signal.SIGUSR1: reload_program_config,
    }

mail_gid = grp.getgrnam('mail').gr_gid
context.gid = mail_gid

important_file = open('spam.data', 'w')
interesting_file = open('eggs.data', 'w')
context.files_preserve = [important_file, interesting_file]

initial_program_setup()

with context:
    do_main_program()