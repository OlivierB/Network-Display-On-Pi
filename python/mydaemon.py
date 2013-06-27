#!/usr/bin/env python

import sys, time
from core.daemon import Daemon

class MyDaemon(Daemon):
	def __init__(self):
		Daemon.__init__(self, '/tmp/daemon-example.pid', stdout='/tmp/out', stderr='/tmp/err')

	def run(self):
		while True:
			time.sleep(1)
			print "eeee"

if __name__ == "__main__":
	daemon = MyDaemon()
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)