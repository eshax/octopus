#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import urllib
import hmac
import hashlib
import base64
import json

'''
火币

api doc:
    https://huobiapi.github.io/docs/spot/v1/cn/#api

'''


class huobi:

    api = 'https://api.huobi.pro'
    api_key = 'c663ff43-ecbd2ab6-0cf99e68-12cf0'
    api_secret = 'c1e4c567-78cd05ad-7393d405-5ba0c'
    api_id = 7352186
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    symbols = {
        "eth/usdt": "ethusdt",
        "btc/usdt": "btcusdt",
        "ltc/usdt": "ltcusdt",
        "eos/usdt": "eosusdt",
        "xrp/usdt": "xrpusdt",
        "bchabc/usdt": "bchusdt",
        "neo/usdt": "neousdt",
        "xmr/usdt": "xmrusdt",
        "etc/usdt": "etcusdt",
        "dash/usdt": "dashusdt",
        "trx/usdt": "trxusdt",
        "ht/usdt": "htusdt",

        "eth/btc": "ethbtc",
        "xrp/btc": "xrpbtc",
        "bchabc/btc": "bchbtc",
        "ltc/btc": "ltcbtc",
        "etc/btc": "etcbtc",
        "eos/btc": "eosbtc",
        "dash/btc": "dashbtc",
        "xmr/btc": "xmrbtc",
        "trx/btc": "trxbtc",
        "ht/btc": "htbtc",

        "eos/eth": "eoseth",
        "xmr/eth": "xmreth",
        "trx/eth": "trxeth",
    }

    @staticmethod
    def sign(path, method, params=None):
        if not params:
            params = {}
        params.update({'AccessKeyId': huobi.api_key,
                       'SignatureMethod': 'HmacSHA256',
                       'SignatureVersion': '2',
                       'Timestamp': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')})
        
        params = sorted(params.items(), key=lambda d: d[0], reverse=False)
        encode_params = urllib.parse.urlencode(params)
        payload = '\n'.join([method, 'api.huobi.pro', path, encode_params]).encode(encoding='UTF8')
        secret_key = huobi.api_secret.encode(encoding='UTF8')
        digest = hmac.new(secret_key, payload,
                          digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(digest)

        params.append(
            ('Signature', signature.decode())
        )

        # if method == 'POST':
        #     p = {}
        #     for param in params:
        #         p[param[0]] = param[1]
        #     return p
        return params

    '''
    帐户信息
    '''
    @staticmethod
    def get_account():
        path = '/v1/account/accounts'
        try:
            response = requests.get(
                huobi.api + path, params=huobi.sign(path, 'GET'))
            if response.status_code == 200:
                print(response.json())
        except:
            pass

    '''
    帐户余额
    '''
    @staticmethod
    def get_balance():
        data = {'exchange': 'huobi'}
        path = '/v1/account/accounts/%s/balance' % huobi.api_id
        try:
            response = requests.get(
                huobi.api + path, params=huobi.sign(path, 'GET'))
            if response.status_code == 200:
                items = response.json().get('data').get('list')
                for item in items:
                    if item.get('type') == 'trade':
                        free = float(item.get('balance'))
                        if free > 0:
                            data[item.get('currency').upper()] = free
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

        path = '/market/depth'
        params = {
            'symbol': huobi.symbols[symbol],
            'type': 'step1'
        }
        try:
            response = requests.get(huobi.api + path, params=params)
            if response.status_code == 200:
                items = response.json().get('tick')
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

    '''
    挂单
    '''
    @staticmethod
    def order(type, symbol, price, amount):
        path = '/v1/order/orders/place'
        params = {
            'account-id': huobi.api_id,
            'symbol': huobi.symbols[symbol],
            'amount': amount,
            'price': price,
            'source': 'api'
        }

        if type == 'buy':
            params['type'] = 'buy-limit'
        else:
            params['type'] = 'sell-limit'
        try:
            response = requests.post(
                huobi.api + path, params=huobi.sign(path, 'POST'), data=json.dumps(params), headers=huobi.headers)
            if response.status_code == 200:
                print(response.json())
                if response.json().get('data'):
                    return True
        except:
            pass
        return False            


if __name__ == '__main__':
    # huobi.get_account()
    huobi.order('buy', 'eth/usdt', 1, 1)
    # print(huobi.get_depth('eth/usdt'))
