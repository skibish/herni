# -*- coding: utf-8 -*-

__author__ = 'Vitaly Raspisenko'

from log_wrapper_module import LogWrapper
from datetime import datetime


class PaymentTransactionLog(object):
    @staticmethod
    def log_transaction(filename, cc_number, price, item_name, description):
        try:
            s = "%s > %s, %.2f, %s, %s\n" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), cc_number[12:], price, item_name, description)
            with open(filename, 'a') as f:
                if isinstance(s, unicode):
                    f.write(s.encode('utf-8'))
                else:
                    f.write(s)
                f.close()
        except:
            LogWrapper().log_trace_back()