from unittest import TestCase
from logic import app
import mock
import json


class TestRestServer(TestCase):

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def tearDown(self):
        pass

    @mock.patch('logic.requests.post')
    def test_initializing(self, post_mock):
        post_mock.return_value.status_code = 200
        post_mock.return_value.text =\
            '{"products": [{"slot": 0, "count": 5, "price": 80, "id": 0, "name": "snickers"}]}'
        data = json.dumps({"filler_url": "url1", "charger_url": "url2"})
        res = self.app.post('/init', data=data, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(post_mock.call_count, 1)
    
    @mock.patch('logic.requests.post')
    def test_product_list(self, post_mock):
        post_mock.return_value.status_code = 200
        post_mock.return_value.text =\
            '{"products": [{"slot": 0, "count": 5, "price": 80, "id": 0, "name": "snickers"}]}'
        data = json.dumps({"filler_url": "url1", "charger_url": "url2"})
        res = self.app.post('/init', data=data, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(post_mock.call_count, 1)
        res = self.app.get('/product_list')
        self.assertEqual(res.data, '{"products": [{"slot": 0, "count": 5, "price": 80, "name": "snickers"}]}')
    
    @mock.patch('logic.requests.post')
    def test_balance_refill(self, post_mock):
        post_mock.return_value.status_code = 200
        post_mock.return_value.text =\
            '{"products": [{"slot": 0, "count": 5, "price": 80, "id": 0, "name": "snickers"}]}'
        data = json.dumps({"filler_url": "url1", "charger_url": "url2"})
        res = self.app.post('/init', data=data, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(post_mock.call_count, 1)
        data = json.dumps({"credit": 100})
        res = self.app.post('/balance_refill', data=data, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, '{"credit": 100}')
    
    @mock.patch('logic.requests.post')
    def test_balance_request(self, post_mock):
        post_mock.return_value.status_code = 200
        post_mock.return_value.text =\
            '{"products": [{"slot": 0, "count": 5, "price": 80, "id": 0, "name": "snickers"}]}'
        data = json.dumps({"filler_url": "url1", "charger_url": "url2"})
        res = self.app.post('/init', data=data, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(post_mock.call_count, 1)
        data = json.dumps({"credit": 100})
        res = self.app.post('/balance_refill', data=data, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, '{"credit": 100}')
        data = json.dumps({"credit": 20})
        res = self.app.post('/balance_refill', data=data, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, '{"credit": 120}')
        res = self.app.get('/balance')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, '{"credit": 120}')
    
    @mock.patch('logic.requests.post')
    def test_balance_return(self, post_mock):
        post_mock.return_value.status_code = 200
        post_mock.return_value.text =\
            '{"products": [{"slot": 0, "count": 5, "price": 80, "id": 0, "name": "snickers"}]}'
        data = json.dumps({"filler_url": "url1", "charger_url": "url2"})
        res = self.app.post('/init', data=data, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(post_mock.call_count, 1)
        data = json.dumps({"credit": 100})
        res = self.app.post('/balance_refill', data=data, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, '{"credit": 100}')
        data = json.dumps({"credit": 20})
        res = self.app.post('/balance_refill', data=data, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, '{"credit": 120}')
        res = self.app.get('/balance_return')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, '{"credit": 0}')
    
    @mock.patch('logic.requests.post')
    def test_slot_refill(self, post_mock):
        post_mock.return_value.status_code = 200
        post_mock.return_value.text =\
            '{"products": []}'
        data = json.dumps({"filler_url": "url1", "charger_url": "url2"})
        res = self.app.post('/init', data=data, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(post_mock.call_count, 1)
        data = '{"product": {"slot": 0, "count": 10, "price": 75, "id": 0, "name": "cookies"}}'
        res = self.app.post('/slot_refill', data=data, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        res = self.app.get('/product_list')
        self.assertEqual(res.data, '{"products": [{"slot": 0, "count": 10, "price": 75, "name": "cookies"}]}')

    @mock.patch('logic.requests.post')
    def test_purchase(self, post_mock):
        post_mock.return_value.status_code = 200
        post_mock.return_value.text =\
            '{"products": [{"slot": 0, "count": 5, "price": 80, "id": 0, "name": "snickers"}]}'
        data = json.dumps({"filler_url": "url1", "charger_url": "url2"})
        res = self.app.post('/init', data=data, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(post_mock.call_count, 1)
        data = json.dumps({"credit": 100})
        res = self.app.post('/balance_refill', data=data, content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, '{"credit": 100}')
        data = json.dumps({"slot": 0, "payment": "cash", "payment_details": {}})
        res = self.app.post('/purchase', data=data, content_type='application/json')
        print res.data
        self.assertEqual(res.data, '{"credit": 20, "result": "success"}')
