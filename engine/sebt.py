#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Single Exchange Bilateral Trading
单交易所双边交易
'''

import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db import db
from utils.ex import ex
from cron.otc import otc
from config import config
from utils.sku import sku

def sebt(exchange, a_symbol, b_symbol, c_symbol, i):

    a_depth = db.redis.hgetall('depth.%s.%s.%s' % (exchange, a_symbol, i))
    b_depth = db.redis.hgetall('depth.%s.%s.%s' % (exchange, b_symbol, i))
    c_depth = db.redis.hgetall('depth.%s.%s.%s' % (exchange, c_symbol, i))

    if a_depth and b_depth and c_depth and float(c_depth['sell_amount']) > 0 and float(b_depth['buy_price']) > 0 and float(b_depth['sell_price']) > 0 and float(a_depth['buy_price']) > 0 :

        fee = ex.get_fee(exchange)
        balance = db.redis.hget('balance.' + exchange, a_symbol.split('/')[1])
        if balance:
            max_amount = float(balance) / float(a_depth['buy_price'])
        else:
            max_amount = 0

        amount = min([float(a_depth['buy_amount']), float(b_depth['sell_amount']), max_amount])
        a_price = float(a_depth['buy_price'])
        b_price = float(b_depth['sell_price'])

        cost = amount * a_price * (1 + fee * 2)
        if a_symbol.split('/')[1] == c_symbol.split('/')[1]:
            rate_price = float(c_depth['sell_price'])
            earn = amount * b_price * rate_price
        else:
            rate_price = float(c_depth['buy_price'])
            earn = amount * b_price / rate_price
        profit = earn - cost

        if profit == 0:
            rate = 0
        else:
            rate = round(profit / cost * 100, 2)
        cnyt_rate = otc.get(a_symbol.split('/')[1], 'buy')
        cnyt_profit = profit * cnyt_rate
        cnyt_cost = cost * cnyt_rate

        if cnyt_cost > 1 and cnyt_profit > 0.5:
            log = '(%s) %s -> %s -> %s 成本:%s 利润:%s 利润率:%s' % (exchange, a_symbol,
                                                                 b_symbol, c_symbol, cost * cnyt_rate, profit * cnyt_rate, str(rate) + '%')
            print(time.strftime("%Y-%m-%d %H:%M:%S"), log, amount)
            doing(exchange, a_symbol, a_price, b_symbol, b_price, amount)

def doing(exchange, a_symbol, a_price, b_symbol, b_price, amount):
    print(exchange, a_symbol, a_price, b_symbol, b_price, amount)
    if sku.buy(exchange, a_symbol, a_price, amount):
        sku.sell(exchange, b_symbol, b_price, amount * (1 - ex.get_fee(exchange)))
        if exchange != 'weidex':
            time.sleep(10)

            



while True:
    print(time.strftime("%Y-%m-%d %H:%M:%S"), '========== SEBT ==========')

    for exchange, symbols in ex.list:
        for a_symbol in symbols:
            for b_symbol in symbols:
                if a_symbol != b_symbol:
                    a_coins = a_symbol.split('/')
                    b_coins = b_symbol.split('/')
                    if a_coins[0] == b_coins[0]:
                        for i in range(config.depth_size):
                            c_symbol = a_coins[1] + '/' + b_coins[1]
                            sebt(exchange, a_symbol, b_symbol, c_symbol, i)
                            # c_symbol = b_coins[1] + '/' + a_coins[1]
                            # sebt(exchange, a_symbol, b_symbol, c_symbol, i)
    time.sleep(10)
