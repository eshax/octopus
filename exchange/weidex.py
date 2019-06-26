#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import random
import time

from jingtum_python_lib.remote import Remote
from jingtum_python_baselib.wallet import Wallet
from jingtum_python_baselib.serializer import Serializer

'''
威链

api doc:
    https://github.com/JCCDex/jcc_server_doc

'''


class weidex:

    api = {
        'ex': [
            'https://ewdjbbl8jgf.jccdex.cn',
            'https://e5e9637c2fa.jccdex.cn',
            'https://e9joixcvsdvi4sf.jccdex.cn',
            'https://eaf28bebdff.jccdex.cn',
            'https://ejid19dcf155a0.jccdex.cn',
            'https://ejii363fa7e9a6.jccdex.cn',
            'https://ejin22b16fbe3e.jccdex.cn',
            'https://ejio68dd7d047f.jccdex.cn',
        ],
        'info': [
            'https://i3b44eb75ef.jccdex.cn',
            'https://i059e8792d5.jccdex.cn',
            'https://i352fb2ef56.jccdex.cn',
            # 'https://ib149d5a1e5.jccdex.cn',
            'https://i8c0429aaeb.jccdex.cn',
            'https://i33a177bdf2.jccdex.cn',
            'https://i1ff1c92a2f.jccdex.cn',
            'https://iujhg293cabc.jccdex.cn',
            'https://iujh6753cabc.jccdex.cn',
            'https://ikj98kyq754c.jccdex.cn',
            'https://il8hn7hcgyxk.jccdex.cn',
        ]
    }

    api_key = 'jKWx6pWumUv7grbTK8CBUpAk4dTCDASzGg'
    api_secret = 'snifFnwDi8siekkKFmXrM5zRtPjxM'

    symbols = {
        'eth/cnyt': 'JETH-CNY',
        'usdt/cnyt': 'JUSDT-CNY',
        'xrp/cnyt': 'JXRP-CNY',
        'moac/cnyt': 'JMOAC-CNY',
        'swtc/cnyt': 'SWT-CNY',
        'jcc/cnyt': 'JJCC-CNY',
        'vcc/cnyt': 'VCC-CNY',
        'csp/cnyt': 'CSP-CNY',
        'slash/cnyt': 'JSLASH-CNY',
        'fst/cnyt': 'JFST-CNY',
        'stm/cnyt': 'JSTM-CNY',
        'call/cnyt': 'JCALL-CNY',

        'eth/usdt': 'JETH-JUSDT',
        'xrp/usdt': 'JXRP-JUSDT',
        'moac/usdt': 'JMOAC-JUSDT',
        'swtc/usdt': 'SWT-JUSDT',
        'fst/usdt': 'JFST-JUSDT',

        'moac/eth': 'JMOAC-JETH',
        'swtc/eth': 'SWT-JETH',

        'xrp/swtc': 'JXRP-SWT',
        'moac/swtc': 'JMOAC-SWT',
        'jcc/swtc': 'JJCC-SWT',
        'vcc/swtc': 'VCC-SWT',
        'csp/swtc': 'CSP-SWT',
        'slash/swtc': 'JSLASH-SWT',
        'stm/swtc': 'JSTM-SWT',
        'call/swtc': 'JCALL-SWT',
    }

    @staticmethod
    def get_api(type, path):
        return random.choice(weidex.api[type]) + path

    '''
    帐户余额
    '''
    @staticmethod
    def get_balance():
        data = {'exchange': 'weidex'}
        path = '/exchange/balances/' + weidex.api_key
        try:
            response = requests.get(weidex.get_api('ex', path))
            if response.status_code == 200:
                items = response.json().get('data')
                for item in items:
                    symbol = item.get('currency')
                    if symbol == 'CNY':
                        symbol = 'CNYT'
                    elif symbol == 'SWT':
                        symbol = 'SWTC'
                    elif symbol[0] == 'J':
                        symbol = symbol[1:]
                    free = float(item.get('value')) - \
                        float(item.get('freezed'))
                    if free > 0:
                        data[symbol] = free
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
        path = '/info/depth/%s/normal' % weidex.symbols[symbol]
        try:
            response = requests.get(weidex.get_api('info', path))
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

    '''
    获取交易序号
    '''
    @staticmethod
    def get_sequence():
        path = '/exchange/sequence/' + weidex.api_key
        try:
            response = requests.get(weidex.get_api('ex', path))
            if response.status_code == 200:
                return response.json().get('data').get('sequence')
        except:
            pass
        return False

    '''
    挂单
    '''
    @staticmethod
    def order(type, symbol, price, amount):

        # 交易币种
        symbols = weidex.symbols[symbol]
        symbols = symbols.split('-')

        o = {
            "Flags": 0,
            "Fee": 0.00001,
            "Account": weidex.api_key,
            "TransactionType": 'OfferCreate',
            "TakerGets": {
                "issuer": 'jGa9J9TkqtBcUoHe2zqhVFFbgUVED6o9or'
            },
            "TakerPays": {
                "issuer": "jGa9J9TkqtBcUoHe2zqhVFFbgUVED6o9or"
            }
        }

        # 交易类型
        if type.lower() == 'buy':
            # buy 买
            o['Flags'] = 0
            o['TakerGets']['value'] = price * amount
            o['TakerGets']['currency'] = symbols[1]
            o['TakerPays']['value'] =  amount
            o['TakerPays']['currency'] = symbols[0]
        else:
            # sell 卖
            o['Flags'] = 524288
            o['TakerGets']['value'] = amount
            o['TakerGets']['currency'] = symbols[0]
            o['TakerPays']['value'] =  price * amount
            o['TakerPays']['currency'] = symbols[1]

        w = Wallet(weidex.api_secret)

        o['Sequence'] = weidex.get_sequence()
        o['SigningPubKey'] = w.get_public_key()
        prefix = 0x53545800
        serial = Serializer(None)
        hash = serial.from_json(o).hash(prefix)
        o['TxnSignature'] = w.sign(hash)

        data = {}
        data['sign'] = serial.from_json(o).to_hex()

        path= '/exchange/sign_order'

        try:
            response = requests.post(weidex.get_api('ex', path), data)
            if response.status_code == 200:
                print(response.json())
                if response.json().get('code') == '0':
                    time.sleep(10)
                    return True
        except:
            pass
        
        return False


if __name__ == '__main__':
    print(weidex.get_depth('swtc/cnyt'))
