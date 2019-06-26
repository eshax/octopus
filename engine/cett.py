#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Cross Exchange Triangular Trade
跨交易所三角交易
'''

import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db import db
from utils.ex import ex
from cron.otc import otc
from config import config

def cett(a_ex, b_ex, a_symbol, b_symbol, i):

    a_depth = db.redis.hgetall('depth.%s.%s.%s' % (a_ex, a_symbol, i))
    b_depth = db.redis.hgetall('depth.%s.%s.%s' % (b_ex, b_symbol, 1))

    if a_depth and b_depth:
        pass

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
                            cett(a_ex, b_ex, a_symbol, b_symbol, z)
