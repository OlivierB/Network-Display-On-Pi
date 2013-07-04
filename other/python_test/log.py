#!/usr/bin/python

# import logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

# logger.info('Start reading database')
# # read database here
# records = {'john': 55, 'tom': 66}
# logger.debug('Records: %s', records)
# logger.info('Updating records ...')
# # update records here
# logger.info('Finish updating records')


import logging, sys
import logging.handlers

def conf_logger():
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)
	# create a file handler
	file_handler = logging.handlers.RotatingFileHandler('hello.log','a', 1000000)
	file_handler.setLevel(logging.DEBUG)
	# output handler
	stdout_handler = logging.StreamHandler(sys.stdout)

	# create a logging format
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	file_handler.setFormatter(formatter)
	stdout_handler.setFormatter(formatter)
	# add the handlers to the logger
	logger.addHandler(stdout_handler)
	logger.addHandler(file_handler)


def test():
	logger = logging.getLogger(__name__)
	logger.info('TEST')


# conf_logger()
# test()
# logger = logging.getLogger(__name__)
# logger.info('Hello baby')
# # read database here
# records = {'john': 55, 'tom': 66}
# logger.debug('Records: %s', records)
# logger.info('Updating records ...')
# # update records here
# logger.info('Finish updating records')

