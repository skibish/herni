# -*- coding: utf-8 -*-

__author__ = 'Vitaly Raspisenko'

import os
import logging
import re
from payment_svc_exception import PaymentSvcException
from twisted.internet import reactor
from twisted.web.server import Site
from log_wrapper_module import LogWrapper
from configobj import ConfigObj
from payment_handler import PaymentHandlerServer


def get_conf_settings():
    return ConfigObj(os.path.basename(__file__).split('.')[:-1][0]+'.conf')


def check_conf_settings(sett):
    if sett['svc']['ip'] != '' and re.match('^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
                                            '(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', sett['svc']['ip']) is None:
        raise PaymentSvcException(errname='TechnicalError', errcode=1, message='Техническая ошибка.',
                                  description="IP address '%s' in configuration file does not match "
                                              "IPV4 format." % sett['svc']['ip'])

    if re.match('^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$',
                sett['svc']['port']) is None:
        raise PaymentSvcException(errname='TechnicalError', errcode=2, message='Техническая ошибка.',
                                  description="Invalid port number '%s' in configuration file." % sett['svc']['port'])

    return sett


def main():
    try:
        c = get_conf_settings()
        sett = check_conf_settings(c)
        reactor.listenTCP(port=int(sett['svc']['port']),
                          factory=Site(PaymentHandlerServer()), interface=sett['svc']['ip'])
        reactor.run()
    except:
        LogWrapper().log_trace_back()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        filename=os.path.basename(__file__).split('.')[:-1][0]+'.log',
                        filemode='a', datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)-15s> %(name)s %(levelname)s %(message)s')
    main()