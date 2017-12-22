#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:lewsan
import logging

logging.basicConfig(filename='logger.log', level=logging.INFO)
logging.debug('debug message')
logging.info('info message')
logging.warn('warn message')
logging.error('error message')
logging.critical('critical message')

logger = logging.getLogger()
print logger

fh = logging.FileHandler('mylogger.log')
logger_1 = logging.getLogger('mylogger')
logger_1.addHandler(fh)
logger_1.info('dadada')
logger_1_1 = logging.getLogger('mylogger.child1')
logger_1_1.info('aaaaaaa')
print logger_1, logger_1_1, logger_1.getChild('child1')
