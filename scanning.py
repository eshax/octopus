#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import threading
import logging
import sys

logging.getLogger("urllib3").setLevel(logging.WARNING)

from utils.ex import ex
from utils.db import db
from cron.otc import otc
from config import config

def get_depth(exchange, symbol):
    depths = ex.get_depth(exchange, symbol, config.depth_size)
    for i in range(len(depths)):
        depth = depths[i]
        for item in depth:
            db.redis.hset('depth.%s.%s.%s' % (exchange, symbol, i), item, depth[item])
        coins = symbol.split('/')
        rate = otc.get(coins[1], 'buy')
        db.redis.hset('depth.%s.%s.%s' % (exchange, symbol, i), 'buy_price_cnyt', float(depth['buy_price']) * rate)
        db.redis.hset('depth.%s.%s.%s' % (exchange, symbol, i), 'sell_price_cnyt', float(depth['sell_price']) * rate)
        # db.redis.hset('depth.%s.%s' % (coins[0], 'buy'), '%s.%s' % (exchange, symbol), float(depth['buy_price']) * rate)
        # db.redis.hset('depth.%s.%s' % (coins[0], 'sell'), '%s.%s' % (exchange, symbol), float(depth['sell_price']) * rate)

        print(exchange, symbol)
        print(db.redis.hgetall('depth.%s.%s.%s' % (exchange, symbol, i)))
        # print(db.redis.hgetall('depth.%s.%s' % (coins[0], 'buy')))
        # print(db.redis.hgetall('depth.%s.%s' % (coins[0], 'sell')))

while True:
    print(time.strftime("%Y-%m-%d %H:%M:%S"), '-------------------- Scanning --------------------')

    for exchange, symbols in ex.list:
        for symbol in symbols:
            threading.Thread(target=get_depth, args=(exchange, symbol)).start()
    time.sleep(5)