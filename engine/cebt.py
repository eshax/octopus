#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Cross Exchange Bilateral Trade
跨交易所双边交易
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

def cebt(a_ex, b_ex, a_symbol, b_symbol, i):
    a_depth = db.redis.hgetall('depth.%s.%s.%s' % (a_ex, a_symbol, i))
    b_depth = db.redis.hgetall('depth.%s.%s.%s' % (b_ex, b_symbol, i))

    if a_depth and b_depth and float(a_depth['buy_amount']) > 0 and float(b_depth['sell_amount']) > 0:
        a_fee = ex.get_fee(a_ex)
        b_fee = ex.get_fee(b_ex)
        balance = db.redis.hget('balance.' + b_ex, b_symbol.split('/')[0])
        if balance is None:
            balance = 0
        amount = min([float(a_depth['buy_amount']), float(b_depth['sell_amount']), float(balance)])
        a_price = float(a_depth['buy_price'])
        b_price = float(b_depth['sell_price'])

        cost = amount * a_price * (1 + a_fee) * otc.get(a_symbol.split('/')[1], 'buy')
        earn = amount * b_price * (1 - b_fee) * otc.get(b_symbol.split('/')[1], 'buy')
        profit = earn - cost

        if profit == 0:
            rate = 0
        else:
            rate = round(profit / cost * 100, 2)
        
        if cost > 1 and profit > 0.5:
            log = '(%s) %s -> (%s) %s 成本:%s 利润:%s 利润率:%s' % (a_ex, a_symbol, b_ex, b_symbol, cost, profit, str(rate) + '%')
            print(time.strftime("%Y-%m-%d %H:%M:%S"), log, amount)
            doing(a_ex, a_symbol, a_price, b_ex, b_symbol, b_price, amount)

def doing(a_ex, a_symbol, a_price, b_ex, b_symbol, b_price, amount):
    print(a_ex, a_symbol, a_price, b_ex, b_symbol, b_price, amount)
    if sku.sell(b_ex, b_symbol, b_price, amount):
        sku.buy(a_ex, a_symbol, a_price, amount)
        if a_ex != 'weidex':
            time.sleep(10)

        


while True:
    print(time.strftime("%Y-%m-%d %H:%M:%S"), '========== CEBT ==========')

    for i in range(len(ex.list)):
        a_ex = ex.list[i][0]
        for j in range(i + 1, len(ex.list)):
            b_ex = ex.list[j][0]
            for a_symbol in ex.list[i][1]:
                for b_symbol in ex.list[j][1]:
                    if a_symbol.split('/')[0] == b_symbol.split('/')[0]:
                        for z in range(config.depth_size):
                            cebt(a_ex, b_ex, a_symbol, b_symbol, z)
    time.sleep(10)
