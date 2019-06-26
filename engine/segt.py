#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Single Exchange Grid Trading
单交易所网格交易
'''

import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db import db
from utils.ex import ex
from cron.otc import otc
from config import config


def segt(exchange, symbol, i):
    depth = db.redis.hgetall('depth.%s.%s.%s' % (exchange, symbol, i))

    if depth:
        pass


while True:
    print(time.strftime("%Y-%m-%d %H:%M:%S"), '========== SEGT ==========')

    for exchange, symbols in ex.list:
        for symbol in symbols:
            for i in range(config.depth_size):
                segt(exchange, symbol, i)
