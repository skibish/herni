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

class PaymentHandlerServer(Resource, LogWrapper):
    isLeaf = True

    def __init__(self):
        cc = ConfigObj('credit-cards.dat')
        cc['cc1'] = {'bank': 'Swedbank', 'ccnum': '1234567891234567', 'pin': '1000', 'balance': 55.42}
        cc['cc2'] = {'bank': 'DNB', 'ccnum': '1234567891234568', 'pin': '2000', 'balance': 0.12}
        cc['cc3'] = {'bank': 'Krajbanka', 'ccnum': '1234567891234569', 'pin': '3000', 'balance': 1.22}
        cc.write()

    def render(self, request):
        operations = ['POST', 'GET']
        try:
            if re.match('/payment/?$', request.path):
                if str(request.method).upper() not in operations:
                    raise PaymentSvcException(errname='TechnicalError', errcode=3, message='Техническая ошибка.',
                                              description="Method %s is not allowed for this service." % request.method)
                if str(request.method).upper() == 'POST':
                    content = request.content.getvalue()
                    response = CreditCardPayment(content).make_payment()
                else:
                    request.setHeader('Content-Type', 'text/html')
                    return '''<!DOCTYPE html>
<html lang="ru">
<head>
    <title>Модуль payment cистемы продажи herni.</title>
    <meta name="author" content="4501MV" />
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <style type="text/css">
        h1 { font-size: 14px; font-family: 'Segoe UI', Arial; color: #333366; }
        body { font-size: 12px; }
    </style>
</head>
<body>
    <h1>Модуль обработки платёжных транзакций payment cистемы продажи herni.</h1>
    <ol>
        <li>Пример сообщения-запроса на выполнение платёжной транзакции:<br />
        {'ccnum': '1234567891234567', 'pin': '1000', 'name': 'СНИКЕРС', 'description': 'payment for food', 'price': 12.35}</li>
    </ol>
</body>
</html>'''
            else:
                raise PaymentSvcException(errname='TechnicalError', errcode=7, message='Техническая ошибка.',
                                          description="The service does not exist." % request.path)

        except PaymentSvcException as e:
            self.log_trace_back()
            response = {'success': False, 'error': e.errname, 'message': e.message, 'description': e.description}
            request.setResponseCode(http.NOT_ALLOWED)
        except:
            self.log_trace_back()
            response = {'success': False, 'error': 'TechnicalError',
                        'message': 'Техническая ошибка.', 'description': 'Please view log file'}

        request.setHeader("content-type", "application/json")

        response_uni = json.dumps(response, ensure_ascii=False, encoding='utf8')
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


class CreditCardPayment(GlobalContentReader):
    def __init__(self, content):
        self.content = content

    def read_content(self):
        data = self.content2json()

        if not re.match('^([0-9]{4}){4}$', data['ccnum']):
            raise PaymentSvcException(errname='InvalidRequestParameters', errcode=1,
                                      message='Номер карты не соответствует формату.',
                                      description='Credit Card number does not fit format.')
        elif not re.match('^[0-9]{4}$', data['pin']):
            raise PaymentSvcException(errname='InvalidRequestParameters', errcode=2,
                                      message='Pin код не соответствует формату.',
                                      description='Pin code does not fit format.')
        elif float(data['price']) < 0.1 or float(data['price']) >= 100:
            raise PaymentSvcException(errname='InvalidRequestParameters', errcode=3,
                                      message='Цена выходит за рамки дозволенной от 0.1 до 20.00 Eur.',
                                      description='The price is out of allowed range from 0.1 to 20.00 Eur.')

        return data

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
