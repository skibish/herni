import json
import requests
from flask import Flask, request
app = Flask(__name__)


slots = []
slot_count = 12
slot_capacity = 10
filler_url = ""
charger_url = ""
session = None


class Product:

    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = price


class Slot:

    def __init__(self, number, capacity):
        self.number = number
        self.capacity = capacity
        self.used_slots = 0
        self.product = None

    def fill(self, product, qty):
        if self.used_slots != 0:
            return 0
        self.product = product
        if qty > self.capacity:
            self.used_slots = self.capacity
        else:
            self.used_slots = qty
        return self.used_slots

    def get_price(self):
        return self.product.price

    def get_name(self):
        return self.product.name

    def issue(self):
        if self.used_slots == 0:
            return False
        self.used_slots -= 1
        if self.used_slots == 0:
            url = filler_url + '/empty'
            data = {'slot': self.number, 'capacity': self.capacity, 'product_id': self.product.product_id}
            headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
            r = requests.post(url, data=json.dumps(data), headers=headers)
            if r.status_code != 200:
                raise Exception("Filler returned %d" % r.status_code)
        return True

    def to_dict(self):
        data = {'slot': self.number,
                'name': self.product.name,
                'price': self.product.price,
                'count': self.used_slots}
        return data


class Session:

    def __init__(self):
        self.balance = 0

    def get_balance(self):
        return self.balance

    def add_balance(self, amount):
        self.balance += amount

    def return_balance(self):
        self.balance = 0

    def pay(self, price):
        if self.balance < price:
            return False
        self.balance -= price
        return True


class RestServer:

    def __init__(self):
        pass

    # UI
    # {"filler_url": "http://127.0.0.1:4568"}
    @staticmethod
    @app.route('/init', methods=['POST'])
    def init():
        global session
        global slot_count
        global slot_capacity
        global filler_url
        global charger_url
        print "Initializing..."
        session = Session()
        for i in range(0, slot_count):
            slots.append(Slot(i, slot_capacity))
        data = request.get_json(silent=True)
        filler_url = data['filler_url']
        charger_url = data['charger_url']
        url = filler_url + '/initial_fill'
        data = {'slots': slot_count, 'capacity': slot_capacity}
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        print "Requesting product list from Filler"
        r = requests.post(url, data=json.dumps(data), headers=headers)
        if r.status_code != 200:
            return "Filler returned %d" % r.status_code
        resp = json.loads(r.text)
        for item in resp['products']:
            p = Product(item['id'], item['name'], item['price'])
            slot_num = item['slot']
            count = item['count']
            slots[slot_num].fill(p, count)
            print 'Added %d %s to slot %d' % (count, item['name'], slot_num)
        print "Initialization done"
        return ""

    # UI
    @staticmethod
    @app.route('/product_list', methods=['GET'])
    def product_list():
        products = []
        for s in slots:
            if s.used_slots != 0:
                products.append(s.to_dict())
        print "Product list"
        data = {'products': products}
        return json.dumps(data)

    # UI
    @staticmethod
    @app.route('/balance', methods=['GET'])
    def balance():
        global session
        if session is None:
            return "Logic not initialized", 500
        print "Current balance: %d" % session.get_balance()
        data = {'credit': session.get_balance()}
        return json.dumps(data)

    # UI
    @staticmethod
    @app.route('/balance_refill', methods=['POST'])
    def balance_refill():
        global session
        if session is None:
            return "Logic not initialized", 500
        data = request.get_json(silent=True)
        session.add_balance(data['credit'])
        print "Added %d to the balance" % data['credit']
        resp = {'credit': session.get_balance()}
        return json.dumps(resp)

    # UI
    @staticmethod
    @app.route('/balance_return', methods=['GET'])
    def balance_return():
        global session
        if session is None:
            return "Logic not initialized", 500
        session.return_balance()
        print "Balance returned"
        resp = {'credit': session.get_balance()}
        return json.dumps(resp)

    # UI
    @staticmethod
    @app.route('/purchase', methods=['POST'])
    def purchase():
        global session
        if session is None:
            print "Logic not initialized"
            return "Logic not initialized", 500
        data = request.get_json(silent=True)
        if data['slot'] >= slot_count:
            print "Bad slot number. Expected 0 - %d" % slot_count
            return "Bad slot"
        slot = data['slot']
        res = 'fail'
        if data['payment'] == 'cash':
            price = slots[slot].get_price()
            if session.get_balance() >= price:
                if slots[slot].issue() and session.pay(price):
                    res = 'success'
                else:
                    print "Purchase issuing failed"
            else:
                print "Balance is too low"
                res = 'low balance'
        elif data['payment'] == 'card':
            card_num = data['payment_details']['ccnum']
            pin = data['payment_details']['pin']
            req = {"ccnum": card_num,
                   "pin": pin,
                   "name": slots[slot].get_name(),
                   "description": "payment for food",
                   "price": slots[slot].get_price()}
            url = charger_url + "/payment"
            headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
            r = requests.post(url, data=json.dumps(req), headers=headers)
            if r.status_code != 200:
                return "Charger returned %d" % r.status_code
            resp = json.loads(r.text)
            if resp['success']:
                if slots[slot].issue():
                    res = 'success'
                else:
                    print "Purchase issuing failed"
            else:
                print "Card payment failed"

        result = {"result": res, "credit": session.get_balance()}
        return json.dumps(result)

    # Filler
    @staticmethod
    @app.route('/slot_refill', methods=['POST'])
    def slot_refill():
        data = request.get_json(silent=True)
        data = data['product']
        p = Product(data['id'], data['name'], data['price'])
        slot_num = data['slot']
        count = data['count']
        slots[slot_num].fill(p, count)
        print 'Refilled %d %s to slot %d' % (count, data['name'], slot_num)
        return ""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4567)
