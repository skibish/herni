# -*- coding: utf-8 -*-

__author__ = 'Vitaly Raspisenko'


import json
import re
from log_wrapper_module import LogWrapper
from twisted.web.resource import Resource
from twisted.web import http
from configobj import ConfigObj
from payment_svc_exception import PaymentSvcException
from payment_transaction_log import PaymentTransactionLog

# class RootResource(Resource):
#     def __init__(self, messageStore):
#         self.messageStore = messageStore
#         Resource.__init__(self)
#         self.putChild('check', CheckMessageHandler(self.messageStore))
#         self.putChild('train', TrainHandler(self.messageStore))
#         self.putChild('delete', RemoveMessageHandler(self.messageStore))
#
#     def getChild(self, path, request):
#         return ShowMessage(self.messageStore, "")


class PaymentHandlerServer(Resource):
    isLeaf = True

    def __init__(self, strategy=None):
        cc = ConfigObj('credit-cards.dat')
        cc['cc1'] = {'bank': 'Swedbank', 'ccnum': '1234567891234567', 'pin': '1000', 'balance': 55.42}
        cc['cc2'] = {'bank': 'DNB', 'ccnum': '1234567891234568', 'pin': '2000', 'balance': 0.12}
        cc['cc3'] = {'bank': 'Krajbanka', 'ccnum': '1234567891234569', 'pin': '3000', 'balance': 1.22}
        cc.write()

    def render(self, request):
        operations = ['POST', 'GET']
        resp = ResponseWrapper()

        if str(request.method).upper() not in operations:
            response = {'success': False, 'error': 'TechnicalError', 'message': 'Техническая ошибка.',
                        'description': "Method %s is not allowed for this service." % request.method}
            resp.set_strategy(ResponseArray(response))

        elif re.match('/payment/?$', request.path):
            if str(request.method).upper() == 'POST':
                resp.set_strategy(ResponseMakePayment())
            else:
                resp.set_strategy(ResponsePaymentServiceIndex())

        else:
            response = {'success': False, 'error': 'TechnicalError', 'message': 'Техническая ошибка.',
                        'description': "The service does not exist. %s" % request.path}
            resp.set_strategy(ResponseArray(response))

        return resp.get_response(request)


class ResponseWrapper(LogWrapper):
    def __init__(self, strategy=None):
        self.action = None
        if strategy:
            self.action = strategy

    def set_strategy(self, strategy):
        self.action = strategy

    def get_response(self, request):
        try:
            if self.action:
                return self.action.get_response(request)
            else:
                raise PaymentSvcException(errname='TechnicalError', errcode=5, message='Техническая ошибка.',
                                          description='Не указан обработчик запроса')
        except PaymentSvcException as e:
            self.log_trace_back()
            return ResponseException(e).get_response(request)
        except:
            self.log_trace_back()
            response = {'success': False, 'error': 'TechnicalError', 'message': 'Техническая ошибка.',
                        'description': 'Please view log file'}
            return ResponseArray(response).get_response(request)


class ResponsePaymentServiceIndex(object):
    @staticmethod
    def get_response(request):
        with open('payment_index.html', 'r') as f:
            return f.read()


class ResponseMakePayment(object):
    @staticmethod
    def get_response(request):
        response = CreditCardPayment(request.content.getvalue()).make_payment()
        return ResponseArray(response).get_response(request)


class ResponseException(object):
    def __init__(self, ex):
        self.ex = ex

    def get_response(self, request):
        response = {'success': False, 'error': self.ex.errname, 'message': self.ex.message,
                    'description': self.ex.description}
        return ResponseArray(response).get_response(request)


class ResponseArray(object):
    def __init__(self, arr):
        self.arr = arr

    def get_response(self, request):
        request.setHeader("content-type", "application/json")
        response_uni = json.dumps(self.arr, ensure_ascii=False, encoding='utf8')
        response_utf = response_uni.encode('utf-8')
        return response_utf


class GlobalContentReader(LogWrapper):
    def content2json(self):
        if self.content is None or self.content == '':
            raise PaymentSvcException(errname='TechnicalError', errcode=4, message='Техническая ошибка.',
                                      description='Пустой запрос.')
        try:
            data = json.loads(self.content)
        except:
            self.log_trace_back()
            raise PaymentSvcException(errname='TechnicalError', errcode=5, message='Техническая ошибка.',
                                      description='Тело запроса не в json формате. content=%s' % self.content)

        return data


class CreditCardPaymentValidator(object):
    @staticmethod
    def validate(data):
        CreditCardPaymentValidateCCNo.validate(data)
        CreditCardPaymentValidatePin.validate(data)
        CreditCardPaymentValidatePrice.validate(data)
        return data


class CreditCardPaymentValidateCCNo(object):
    @staticmethod
    def validate(data):
        if not re.match('^([0-9]{4}){4}$', data['ccnum']):
            raise PaymentSvcException(errname='InvalidRequestParameters', errcode=1,
                                      message='Номер карты не соответствует формату.',
                                      description='Credit Card number does not fit format.')


class CreditCardPaymentValidatePin(object):
    @staticmethod
    def validate(data):
        if not re.match('^[0-9]{4}$', data['pin']):
            raise PaymentSvcException(errname='InvalidRequestParameters', errcode=2,
                                      message='Pin код не соответствует формату.',
                                      description='Pin code does not fit format.')


class CreditCardPaymentValidatePrice(object):
    @staticmethod
    def validate(data):
        if float(data['price']) < 0.1 or float(data['price']) >= 100:
            raise PaymentSvcException(errname='InvalidRequestParameters', errcode=3,
                                      message='Цена выходит за рамки дозволенной от 0.1 до 20.00 Eur.',
                                      description='The price is out of allowed range from 0.1 to 20.00 Eur.')

class CreditCardPayment(GlobalContentReader):
    def __init__(self, content):
        self.content = content

    def read_content(self):
        return CreditCardPaymentValidator.validate(self.content2json())

    def make_payment(self):
        data = self.read_content()

        cc = ConfigObj('credit-cards.dat')

        c = ''
        for a in cc:
            if 'ccnum' in cc[a]:
                if cc[a]['ccnum'] == data['ccnum']:
                    c = a
                    break

        if c == '':
            raise PaymentSvcException(errname='AccountError', errcode=1, message='Кредитная карта отклонена.',
                                      description='Credit Card was rejected.')
        elif cc[c]['pin'] != data['pin']:
            raise PaymentSvcException(errname='AccountError', errcode=2, message='Неправильный pin-код.',
                                      description='Incorrect pin-code.')
        elif float(cc[c]['balance']) < float(data['price']):
            raise PaymentSvcException(errname='AccountError', errcode=3, message='Не достаточно средств на счету.',
                                      description='Not enough funds on account.')
        elif cc[c]['bank'] == 'Krajbanka':
            raise PaymentSvcException(errname='TechnicalError', errcode=6, message='Нет связи с банком.',
                                      description='Communication error.')

        cc[c]['balance'] = float(cc[c]['balance']) - float(data['price'])

        cc.write()

        PaymentTransactionLog.log_transaction('transaction.log',
                                              data['ccnum'], data['price'], data['name'], data['description'])

        return {'success': True, 'message': 'Платёж успешно выполнен.',
                'description': 'Payment has been successfully made.'}
