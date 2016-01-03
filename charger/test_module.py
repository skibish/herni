# -*- coding: utf-8 -*-

__author__ = 'Vitaly Raspisenko'

import unittest


class TestRestMethods(unittest.TestCase):
    def test_charger_settings(self):
        import payment_svc
        import payment_svc_exception

        """Test that conf has all parameters"""
        sett = payment_svc.get_conf_settings()
        self.assertTrue('svc' in sett)
        self.assertTrue('port' in sett['svc'])
        self.assertTrue('ip' in sett['svc'])

        """Test that all is good"""
        try:
            payment_svc.check_conf_settings(sett)
        except payment_svc_exception.PaymentSvcException:
            self.fail("check_conf_settings(sett) raised PaymentSvcException unexpectedly!")

        """Test that ip has wrong format"""
        ip = sett['svc']['ip']
        sett['svc']['ip'] += 'abc'
        with self.assertRaises(payment_svc_exception.PaymentSvcException) as cm:
            payment_svc.check_conf_settings(sett)
        the_exception = cm.exception
        self.assertEqual(the_exception.errcode, 1)

        """Test that port has invalid values"""
        sett['svc']['ip'] = ip
        sett['svc']['port'] = str(int(sett['svc']['port']) + 65535)
        with self.assertRaises(payment_svc_exception.PaymentSvcException) as cm:
            payment_svc.check_conf_settings(sett)
        the_exception = cm.exception
        self.assertEqual(the_exception.errcode, 2)

    def test_charger_availability(self):
        import requests
        r = requests.get('http://127.0.0.1:6082/payment/')
        self.assertEqual(r.status_code, 200)

        with open('payment_index.html', 'r') as f:
            s = f.read()
        self.assertEqual(s, r.content)

    def test_charger_payment_request(self):
        import requests
        import json

        url = 'http://127.0.0.1:6082/payment/'
        values = {'ccnum': '1234567891234567',
                  'pin': '1000',
                  'name': 'СНИКЕРС',
                  'description': 'payment for food',
                  'price': 2.35}

        data = json.dumps(values, ensure_ascii=False, encoding='utf8')

        r = requests.post(url, data.encode('utf-8'), {'content-type': 'application/json'})
        self.assertEqual(r.status_code, 200)

        res = json.loads(r.content)
        self.assertEqual(res['success'], True)

    def test_charger_transaction_log(self):
        import payment_transaction_log
        import os
        payment_transaction_log.PaymentTransactionLog.log_transaction('test_log_transaction.log', '0000000000000000',
                                                                      100.23, 'test', 'test')

        with open('test_log_transaction.log', 'r') as f:
            s = f.read()

        os.remove('test_log_transaction.log')

        self.assertEqual(s[22:], "0000, 100.23, test, test\n")

if __name__ == "__main__":
    unittest.main()





    #self.assertEqual('foo'.upper(), 'FOO')