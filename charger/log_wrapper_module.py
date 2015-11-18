# -*- coding: utf-8 -*-

__author__ = 'Vitaly Raspisenko'

import sys
import traceback
import logging


class LogWrapper(object):
    @property
    def logger(self):
        name = '.'.join([__name__, self.__class__.__name__])
        return logging.getLogger(name)

    @staticmethod
    def get_trace_back():
        exc_type, exc_value, exc_traceback = sys.exc_info()
        s = traceback.extract_tb(exc_traceback)
        return "(%s), %s  in file: %s method %s at call %s on line %s" % (str(exc_value), exc_value.__class__, s[0][0], s[0][2], s[0][3], s[0][1])

    def log_trace_back(self):
        s = self.get_trace_back()
        print >> sys.stderr, s
        self.logger.debug(s)