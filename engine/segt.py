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


def segt(conf_path, run=False):

    print("load config:", conf_path)

    with open(conf_path, 'r') as f:

        cf = json.load(f)

        for c in ['exchange', 'apiconfig', 'symbol', 'fluctuate', 'amount']:
            if c not in cf:
                print("config no %s!" % c)
                return

        print(".")
        exchange = cf.get("exchange")
        print("exchange: \t", exchange)
        apiconfig = cf.get("apiconfig")
        print("apiconfig:\t", apiconfig)
        symbol = cf.get("symbol")
        print("symbol:   \t", symbol)
        fluctuate = cf.get("fluctuate")
        print("fluctuate:\t %f" % fluctuate)
        amount = cf.get("amount")
        print("amount:   \t", amount)
        print(".")

        while True:

            # data = depth.get(exchange , symbol)

            data = ex.get_depth(exchange, symbol)

            if data:

                bp = float(data[0]['buy_price'])
                sp = float(data[0]['sell_price'])

                low = format_price(min(bp, sp), fluctuate)
                high = format_price(max(bp, sp), fluctuate)

                '''
                1、监控买一数据的变化
                2、以买一价格为中心
                3、上下挂单, 上挂卖, 下挂买, 共挂 10 单
                4、查询委托列表、不进行重复挂单
                例如:
                    当前买一价格为 0.00725
                    挂买入 0.00724 0.00723 0.00722 0.00721 0.00720
                    挂卖出 0.00726 0.00727 0.00728 0.00729 0.00730
                '''
                if low > 0.0:
                    print(time.strftime("%Y-%m-%d %H:%M:%S"), data, 'low:', low, 'high:', high)
                    print(".")
                    orders = ex.orders(exchange, apiconfig)
                    prices = set([(o['type'], float(o['price'])) for o in orders if o['symbol'] == symbol])
                    print(time.strftime("%Y-%m-%d %H:%M:%S"), "buys:", sorted([y for x, y in prices if x == "buy"]))
                    print(time.strftime("%Y-%m-%d %H:%M:%S"), "sells:", sorted([y for x, y in prices if x == "sell"]))
                    print(".")
                    order_many_list = []
                    for n in range(1, 6):
                        # buy
                        price = format_price((low - (fluctuate * n)), fluctuate)
                        if ('buy', price) not in prices:
                            order_many_list.append(
                                {
                                    "type": "buy",
                                    "symbol": symbol,
                                    "price": price,
                                    "amount": int(amount)
                                }
                            )
                            print(time.strftime("%Y-%m-%d %H:%M:%S"), "[ buy %f ]" % price)
                        # sell
                        price = format_price((low + (fluctuate * n)), fluctuate)
                        if ('sell', price) not in prices:
                            order_many_list.append(
                                {
                                    "type": "sell",
                                    "symbol": symbol,
                                    "price": price,
                                    "amount": int(amount)
                                }
                            )
                            print(time.strftime("%Y-%m-%d %H:%M:%S"), "[ sell %f ]" % price)
                    # execute
                    print(".")
                    ex.order_many(exchange, order_many_list, apiconfig)

                    print(".")
                    print(".")

            if run:
                time.sleep(10)
            else:
                break


if __name__ == '__main__':

    if len(sys.argv) == 3:
        cmd = sys.argv[1]
        if cmd == "start":
            conf_path = sys.argv[2]
            threading.Thread(target=segt, args=(conf_path, True)).start()

    if len(sys.argv) == 2:
        conf_path = sys.argv[1]
        segt(conf_path, False)

    if len(sys.argv) == 1:
        print("usage: python segt.py segt.conf")
        print("usage: python segt.py strat segt.conf")
