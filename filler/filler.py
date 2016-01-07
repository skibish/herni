import json
import thread
import time
import requests
from flask import Flask, request
app = Flask(__name__)


logic_port = "4567"
products = [{"name": "snickers",
             "price": 0.80},
            {"name": "cola",
             "price": 0.100},
            {"name": "water",
             "price": 0.75},
            {"name": "orange juice",
             "price": 0.100},
            {"name": "unknown juice",
             "price": 0.65},
            {"name": "milk",
             "price": 0.85},
            {"name": "Semki",
             "price": 0.77},
            {"name": "nuts",
             "price": 0.120},
            {"name": "waffels",
             "price": 0.110},
            {"name": "banana",
             "price": 0.25},
            {"name": "potato",
             "price": 0.50},
            {"name": "poison",
             "price": 0.45}]

class Singleton:

    def __init__(self, decorated):
        self._decorated = decorated

    def instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)

@Singleton
class Filler:

    def __init__(self):
        pass

    def refill_slot(self, url, data):
        print "Filling after some delay..."
        time.sleep(10)
        print "Filling logic slot %d" % data['product']['slot']
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        if r.status_code != 200:
            raise Exception("Logic returned %d" % r.status_code)


class RestServer:

    def __init__(self):
        pass

    # Logic
    @staticmethod
    @app.route('/initial_fill', methods=['POST'])
    def init():
        print "Received initial fill request from %s" % request.remote_addr
        data = request.get_json(silent=True)
        slots = data['slots']
        capacity = data['capacity']
        prod_list = []
        for i in range(0, slots):
            index = i % len(products)
            d = dict()
            d['id'] = index
            d['name'] = products[index]['name']
            d['price'] = products[index]['price']
            d['slot'] = i
            d['count'] = capacity
            prod_list.append(d)
        print prod_list
        result = {'products': prod_list}
        return json.dumps(result)

    # UI
    @staticmethod
    @app.route('/empty', methods=['POST'])
    def fill():
        data = request.get_json(silent=True)
        url = "http://" + request.remote_addr + ":" + logic_port + "/slot_refill"
        index = data['product_id']
        d = {'product': {'id': index,
                         'name': products[index]['name'],
                         'price': products[index]['price'],
                         'slot': data['slot'],
                         'count': data['capacity']}}
        thread.start_new_thread(Filler.instance().refill_slot, (url, d))
        return ""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4568)
