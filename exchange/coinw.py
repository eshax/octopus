#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
import urllib

# import sys
# import os

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.md5 import md5

'''
币赢

api doc:
    https://www.coinw.ai/api_doc.html

'''


class coinw:

    api     = 'http://api.coinw.ai/appApi.html?'
    api_key     = '1b3342b5-8baf-4669-a1bc-9047ad8b720a'
    api_secret  = '5RAIGRUWKDS2I9VAYI2I4QSZ4HZAIVETUXE1'

    symbols = {
        'btc/cnyt'  : 45,
        'usdt/cnyt' : 59,
        'eth/cnyt'  : 14,
        'eos/cnyt'  : 29,
        'ltc/cnyt'  : 3,
        'trx/cnyt'  : 70,
        'xrp/cnyt'  : 60,
        'xmr/cnyt'  : 94,
        'bchabc/cnyt'  : 69,
        'dash/cnyt'  : 61,
        'moac/cnyt' : 43,
        'swtc/cnyt' : 47,
        'ht/cnyt' : 91,
        'bnb/cnyt' : 85,

        'btc/usdt'  : 78,
        'eth/usdt'  : 79,
        'eos/usdt'  : 84,
        'ltc/usdt'  : 86,
        'trx/usdt'  : 98,
        'xrp/usdt'  : 83,
        'xmr/usdt'  : 113,
        'bchabc/usdt'  : 99,
        'dash/usdt'  : 82,
    }


    '''
    签名
    '''
    @staticmethod
    def sign(path, params = {}):
        params.update({
            'api_key': coinw.api_key,
        })
        params = sorted(params.items(), key=lambda d: d[0], reverse=False)
        sign = md5.encode(urllib.parse.urlencode(params) + '&secret_key=' + coinw.api_secret)
        return coinw.api + path + '&' + urllib.parse.urlencode(params) + '&sign=' + sign.upper()

    '''
    帐户余额
    '''
    @staticmethod
    def get_balance():
        data = {'exchange': 'coinw'}
        path = 'action=userinfo'
        try:
            response = requests.post(coinw.sign(path))
            if response.status_code == 200:
                items = response.json().get('data').get('free')
                for item in items:
                    free = float(items[item])
                    if free > 0:
                        data[item] = free
        except:
            pass
        return data

    '''
    交易深度
    '''
    @staticmethod
    def get_depth(symbol, size = 1):
        depths = [{
            'buy_price': 0,
            'buy_amount': 0,
            'sell_price': 0,
            'sell_amount': 0,
        }]
        path = 'action=depth'
        params = {
            'symbol':coinw.symbols[symbol]
        }
        try:
            response = requests.get(coinw.sign(path, params))
            if response.status_code == 200:
                items = response.json().get('data')
                list = []
                for i in range(size):
                    asks = items.get('asks')[i]
                    bids = items.get('bids')[i]
                    depth = {}
                    depth['buy_price'] = asks['price']
                    depth['buy_amount'] = asks['amount']
                    depth['sell_price'] = bids['price']
                    depth['sell_amount'] = bids['amount']
                    list.append(depth)
                depths = list
        except:
            pass
        return depths

    # '''
    # 挂单
    # '''
    @staticmethod
    def order(type, symbol, price, amount):
        path = 'action=trade'
        params = {
            'symbol': coinw.symbols[symbol],
            'amount': amount,
            'price': price
        }
        if type == 'buy':
            params['type'] = 0
        else:
            params['type'] = 1

        try:
            response = requests.post(coinw.sign(path, params))
            if response.status_code == 200:
                print(response.json())
                if response.json().get('data'):
                    return True    
        except:
            pass
        return False
  


if __name__ == '__main__':
    # print(coinw.get_balance())
    print(coinw.get_depth('moac/cnyt', 2))
    # coinw.order('buy', 'moac/cnyt', 1, 1)
