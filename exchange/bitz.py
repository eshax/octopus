#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import random
import time
import urllib
import json

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.md5 import md5

'''
Bit-Z

api doc:
    https://apidoc.bitz.top/cn/Public/API-Reference.html

'''


class bitz:

    api = [
        # 'https://apiv2.bitz.com',
        'https://apiv2.bit-z.pro',
        'https://api.bitzapi.com',
        'https://api.bitzoverseas.com',
        'https://api.bitzspeed.com',
    ]
    api_key = '42eb6798b7be92da77bd262df0ddbcda'
    api_secret = 'eVK0cxcMJjHPM3H2nWUShfozmoAtYTkx5U98JdeQRVRS507KhgSk4rfH6UnGtZZi'

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"}

    symbols = {
        "btc/usdt"  : "btc_usdt",
        "eth/usdt"  : "eth_usdt",
        "eos/usdt"  : "eos_usdt",
        "trx/usdt"  : "trx_usdt",
        "xrp/usdt"  : "xrp_usdt",
        "ltc/usdt"  : "ltc_usdt",
        "bchabc/usdt"  : "bchabc_usdt",
        "neo/usdt"  : "neo_usdt",
        "bnb/usdt"  : "bnb_usdt",

        "moac/eth" : "moac_eth",
        "swtc/eth" : "swtc_eth",
        "trx/eth" : "trx_eth", 

        "eth/btc"  : "eth_btc",
        "eos/btc"  : "eos_btc",
        "ltc/btc"  : "ltc_btc",
        "dash/btc"  : "dash_btc",
        "bnb/btc"  : "bnb_btc",
    }

    '''
    签名
    '''
    @staticmethod
    def sign(params = {}):
        params.update({
            'apiKey': bitz.api_key,
            'timeStamp': int(time.time()),
        })
        params = dict(sorted(params.items(), key=lambda d: d[0], reverse=False))
        sign = urllib.parse.urlencode(params) + bitz.api_secret
        params['sign'] = md5.encode(sign)
        return params

    '''
    帐户余额
    '''
    @staticmethod
    def get_balance():
        data = {'exchange': 'bitz'}
        path = '/Assets/getUserAssets'
        params = {
            'nonce': str(random.randint(0,999999)).zfill(6)
        }
        try:
            response = requests.post(random.choice(bitz.api) + path, data=bitz.sign(params), headers=bitz.headers)
            if response.status_code == 200:
                if (response.json().get('status') == 200):
                    items = response.json().get('data')
                    print(items)
                    # for item in items:
                    #     free = float(item['available'])
                    #     if free > 0:
                    #         data[item['asset']] = free
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
        path = '/Market/depth?'
        params = {
            'symbol':bitz.symbols[symbol]
        }
        try:
            response = requests.get(random.choice(bitz.api) + path + urllib.parse.urlencode(params), headers=bitz.headers)
            if response.status_code == 200:
                items = response.json().get('data')
                list = []
                for i in range(size):
                    asks = items.get('asks')[i]
                    bids = items.get('bids')[i]
                    depth = {}
                    depth['buy_price'] = asks[0]
                    depth['buy_amount'] = asks[1]
                    depth['sell_price'] = bids[0]
                    depth['sell_amount'] = bids[1]
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
        path = '/Trade/addEntrustSheet'
        params = {
            'symbol': bitz.symbols[symbol],
            'number': amount,
            'price': price,
            'nonce': str(random.randint(0,999999)).zfill(6),
            'tradePwd': '240780'
        }
        if type == 'buy':
            params['type'] = 1
        else:
            params['type'] = 2

        try:
            response = requests.post(random.choice(bitz.api) + path, bitz.sign(params), headers=bitz.headers)
            if response.status_code == 200:
                print(response.json())
                if response.json().get('data'):
                    return True    
        except:
            pass
        return False
  


if __name__ == '__main__':
    pass
    print(bitz.get_balance())
    # print(bitz.get_depth('moac/eth'))
    # bitz.order('buy', 'moac/eth', 1, 0.001)
