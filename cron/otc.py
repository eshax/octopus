#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import logging

logging.getLogger("urllib3").setLevel(logging.WARNING)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

from exchange.weidex import weidex
from utils.db import db


class otc:

    api = 'https://otc-api.eiijo.cn/v1/data/trade-market?country=37&currency=1&payMethod=0&currPage=1&coinId=%s&tradeType=%s&blockType=general&online=1'

    coins = {
        'btc': 1,
        'usdt': 2,
        'eth': 3,
    }

    @staticmethod
    def save():
        db.redis.hset('otc', 'cnyt_buy', 1)
        db.redis.hset('otc', 'cnyt_sell', 1)

        for coin in otc.coins:
            for type in ['buy', 'sell']:
                response = requests.get(otc.api % (otc.coins[coin], type))
                if response.status_code == 200:
                    k = '%s_%s' % (coin, type)
                    data = response.json().get('data')
                    v = data[0]['price']
                    db.redis.hset('otc', k, v)
                    print(k, v)

        swtc = weidex.get_depth('swtc/cnyt')[0]
        print(swtc)
        db.redis.hset('otc', 'swtc_buy', swtc['sell_price'])
        db.redis.hset('otc', 'swtc_sell', swtc['buy_price'])

    @staticmethod
    def get(symbol, type):
        try:
            return float(db.redis.hget('otc', '%s_%s' % (symbol, type)))
        except:
            return 0


if __name__ == '__main__':
    otc.save()
