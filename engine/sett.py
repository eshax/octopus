#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Single Exchange Triangular Trading
单交易所三角交易
'''

import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import config
from cron.otc import otc
from utils.ex import ex
from utils.db import db
from utils.sku import sku

def sett(exchange, a_symbol, b_symbol, c_symbol, type, i):

    a_depth = db.redis.hgetall('depth.%s.%s.%s' % (exchange, a_symbol, i))
    b_depth = db.redis.hgetall('depth.%s.%s.%s' % (exchange, b_symbol, i))
    c_depth = db.redis.hgetall('depth.%s.%s.%s' % (exchange, c_symbol, i))

    if a_depth and b_depth and c_depth and float(c_depth['sell_amount']) > 0 and float(b_depth['buy_price']) > 0 and float(b_depth['sell_price']) > 0:
        fee = ex.get_fee(exchange)
        a_price = float(a_depth['buy_price'])
        c_price = float(c_depth['sell_price'])

        if (type == 'bbs'):
            b_price = float(b_depth['buy_price'])
            amount = [float(a_depth['buy_amount']) / b_price,
                      float(b_depth['buy_amount']), float(c_depth['sell_amount'])]
            # amount = [float(a_depth['buy_amount']) / b_price, float(b_depth['buy_amount'])]
            amount = min(amount)
            a_amount = amount * b_price
            b_amount = amount
            c_amount = amount
        else:
            b_price = float(b_depth['sell_price'])
            amount = [float(a_depth['buy_amount']), float(
                b_depth['sell_amount']), float(c_depth['sell_amount']) / b_price]
            # amount = [float(a_depth['buy_amount']), float(b_depth['sell_amount'])]
            amount = min(amount)
            a_amount = amount
            b_amount = amount
            c_amount = amount * b_price

        cost = a_amount * a_price * (1 + fee * 3)
        earn = c_amount * c_price
        profit = earn - cost

        if profit == 0:
            rate = 0
        else:
            rate = round(profit / cost * 100, 2)

        cnyt_rate = otc.get(a_symbol.split('/')[1], 'buy')
        cnyt_profit = profit * cnyt_rate

        if cnyt_profit > 0:
            log = '(%s) %s %s -> %s -> %s 成本:%s 利润:%s 利润率:%s' % (exchange, type, a_symbol,
                                                                 b_symbol, c_symbol, cost * cnyt_rate, profit * cnyt_rate, str(rate) + '%')
            print(time.strftime("%Y-%m-%d %H:%M:%S"), log, amount)
            doing(exchange, type, a_symbol, a_price, a_amount, b_symbol, b_price, b_amount, c_symbol, c_price, c_amount)

def doing(exchange, type, a_symbol, a_price, a_amount, b_symbol, b_price, b_amount, c_symbol, c_price, c_amount):
    print(exchange, type, a_symbol, a_price, a_amount, b_symbol, b_price, b_amount, c_symbol, c_price, c_amount)
    if sku.buy(exchange, a_symbol, a_price, a_amount):
        ret = False
        if type == 'bbs':
            ret = sku.buy(exchange, b_symbol, b_price, b_amount)
        else:
            ret = sku.sell(exchange, b_symbol, b_price, b_amount)
        if ret:
            sku.sell(exchange, c_symbol, c_price, c_amount)
            if exchange != 'weidex':
                time.sleep(10)

while True:
    print(time.strftime("%Y-%m-%d %H:%M:%S"), '========== SETT ==========')

    for exchange, symbols in ex.list:
        for a_symbol in symbols:
            for b_symbol in symbols:
                if a_symbol != b_symbol:
                    a_coins = a_symbol.split('/')
                    b_coins = b_symbol.split('/')
                    for i in range(config.depth_size):
                        if a_coins[0] == b_coins[1]:
                            c_symbol = b_coins[0] + '/' + a_coins[1]
                            sett(exchange, a_symbol,
                                 b_symbol, c_symbol, 'bbs', i)
                        elif a_coins[0] == b_coins[0]:
                            c_symbol = b_coins[1] + '/' + a_coins[1]
                            sett(exchange, a_symbol,
                                 b_symbol, c_symbol, 'bss', i)
    time.sleep(10)