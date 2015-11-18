# -*- coding: utf-8 -*-

__author__ = 'Vitaly Raspisenko'


class PaymentSvcException(Exception):

    def __init__(self, errname, errcode, message, description):
        self.errname = errname
        self.errcode = errcode
        self.message = message
        self.description = description

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        s = "errcode=%s(%d) %s, %s" % (self.errname, self.errcode, self.message, self.description)
        return s