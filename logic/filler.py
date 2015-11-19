import json
import thread
import time
import requests
from flask import Flask, request
app = Flask(__name__)


logic_port = "4567"
products = [{"name": "snickers",
             "price": 80},
            {"name": "cola",
             "price": 100},
            {"name": "water",
             "price": 75},
            {"name": "orange juice",
             "price": 100},
            {"name": "unknown juice",
             "price": 65},
            {"name": "milk",
             "price": 85},
            {"name": "Semki",
             "price": 77},
            {"name": "nuts",
             "price": 120},
            {"name": "waffels",
             "price": 110},
            {"name": "banana",
             "price": 25},
            {"name": "potato",
             "price": 50},
            {"name": "poison",
             "price": 45}]


def refill_slot(url, data):
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
        result = {'products': prod_list}
        return json.dumps(result)

    # UI
    @staticmethod
    @app.route('/empty', methods=['POST'])
    def product_list():
        data = request.get_json(silent=True)
        url = "http://" + request.remote_addr + ":" + logic_port + "/slot_refill"
        index = data['product_id']
        d = {'product': {'id': index,
                         'name': products[index]['name'],
                         'price': products[index]['price'],
                         'slot': data['slot'],
                         'count': data['capacity']}}
        thread.start_new_thread(refill_slot, (url, d))
        return ""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4568)
