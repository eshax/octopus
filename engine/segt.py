#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Single Exchange Grid Trading
单交易所网格交易
'''
import os, sys, time, threading, json

root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print(root_path)
sys.path.append(root_path)

from octopus.exchange.exchange import exchange as ex
from octopus.market import depth, space, account

def format_price(price, fluctuate):
    for n in range(-10, 10):
        if int(fluctuate * (10 ** n)) > 0:
            break
    return round(float(int(price * (10 ** n))) / (10 ** n), n)


def segt(conf_path):

    print(conf_path)

    try:
        with open(conf_path, 'r') as f:
            cf = json.load(f)

            for c in ['exchange', 'apiconfig', 'symbol', 'fluctuate', 'amount']:
                if c not in cf:
                    print("config no %s!" % c)
                    return

            exchange = cf.get("exchange")
            apiconfig = cf.get("apiconfig")
            symbol = cf.get("symbol")
            fluctuate = cf.get("fluctuate")

            _low, _high = 0.0, 0.0

            while True:

                data = depth.get(exchange , symbol)

                if data:

                    bp = float(data['buy_price'])
                    sp = float(data['sell_price'])

                    low = format_price(min(bp, sp), fluctuate)
                    high = format_price(max(bp, sp), fluctuate)

                    action = "."

                    if low > _low and _low > 0.0:
                        action = "[ buy %f ]" % (low - fluctuate)
                    if low < _low and _low > 0.0:
                        action = "[ sell %f ]" % (low + fluctuate)
                    if high > _high and _high > 0.0:
                        action = "[ buy %f ]" % (high - fluctuate)
                    if high < _high and _high > 0.0:
                        action = "[ sell %f ]" % (high + fluctuate)

                    print(time.strftime("%Y-%m-%d %H:%M:%S"), data, 'low:', low, 'high:', high, action)

                    _low = low
                    _high = high

                time.sleep(1)

    except Exception as e:
        print(e.message)
        print("error config!")

if __name__ == '__main__':

    if len(sys.argv) == 2:
        conf_path = sys.argv[1]
        threading.Thread(target=segt, args=(conf_path,)).start()
    else:
        print("usage: python segt.py segt.conf")
