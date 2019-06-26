#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
import urllib
import json

from utils.md5 import md5

'''
满币

api doc:
    https://github.com/Coinbene/API-Documents-CHN/wiki/0.0.0-Coinbene-API%E6%96%87%E6%A1%A3

'''


class coinbene:

    api     = 'https://api.coinbene.com'
    api_key     = '24f2cba00fc8a3396210369746863282'
    api_secret  = '7c40000b6ecf48feb753c8956df5ab52'

    headers = {
        'Content-type': 'application/json'
    }

    symbols = {
        'btc/usdt'  : 'btcusdt',
        'eth/usdt'  : 'ethusdt',
        'eos/usdt'  : 'eosusdt',
        'bchabc/usdt'  : 'bchabcusdt',
        'trx/usdt'  : 'trxusdt',
        'xrp/usdt'  : 'xrpusdt',
        'ltc/usdt'  : 'ltcusdt',
        'neo/usdt'  : 'neousdt',
        'etc/usdt'  : 'etcusdt',
        'moac/usdt' : 'moacusdt',
        'swtc/usdt' : 'swtcusdt', 

        'eth/btc'   : 'ethbtc',
        'eos/btc'   : 'eosbtc',
        'trx/btc'   : 'trxbtc',
        'xrp/btc'   : 'xrpbtc',
        'ltc/btc'   : 'ltcbtc',
        'xmr/btc'   : 'xmrbtc',
        'neo/btc'   : 'neobtc',
        'etc/btc'   : 'etcbtc',
        
    }


    '''
    签名
    '''
    @staticmethod
    def sign(params = {}):
        params.update({
            'apiid': coinbene.api_key,
            'timestamp': int(round(time.time() * 1000)),
            'secret': coinbene.api_secret
        })
        params = dict(sorted(params.items(), key=lambda d: d[0], reverse=False))
        sign = urllib.parse.urlencode(params).upper()
        params['sign'] = md5.encode(sign)
        del params['secret']
        return json.dumps(params)

    '''
    帐户余额
    '''
    @staticmethod
    def get_balance():
        data = {'exchange': 'coinbene'}
        path = '/v1/trade/balance'
        params = {
            'account': 'exchange',
        }
        try:
            response = requests.post(coinbene.api + path, data=coinbene.sign(params), headers=coinbene.headers)
            if response.status_code == 200:
                items = response.json().get('balance')
                for item in items:
                    free = float(item['available'])
                    if free > 0:
                        data[item['asset']] = free
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
        path = '/v1/market/orderbook?'
        params = {
            'symbol':coinbene.symbols[symbol]
        }
        try:
            response = requests.get(coinbene.api + path + urllib.parse.urlencode(params), headers=coinbene.headers)
            if response.status_code == 200:
                items = response.json().get('orderbook')
                list = []
                for i in range(size):
                    asks = items.get('asks')[i]
                    bids = items.get('bids')[i]
                    depth = {}
                    depth['buy_price'] = asks['price']
                    depth['buy_amount'] = asks['quantity']
                    depth['sell_price'] = bids['price']
                    depth['sell_amount'] = bids['quantity']
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
        path = '/v1/trade/order/place'
        params = {
            'symbol': coinbene.symbols[symbol],
            'quantity': amount,
            'price': price,
        }
        if type == 'buy':
            params['type'] = 'buy-limit'
        else:
            params['type'] = 'sell-limit'

        try:
            response = requests.post(coinbene.api + path, coinbene.sign(params), headers=coinbene.headers)
            if response.status_code == 200:
                print(response.json())
                if response.json().get('orderid'):
                    return True    
        except:
            pass
        return False
  


if __name__ == '__main__':
    pass
    # print(coinbene.get_balance())
    # print(coinbene.get_depth('moac/usdt'))
    # coinbene.order('buy', 'moac/usdt', 1, 0.01)
