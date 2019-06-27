#!/usr/bin/env python
# -*- coding: utf-8 -*-

from exchange.weidex import weidex
from exchange.huobi import huobi
from exchange.coinw import coinw
from exchange.coinbene import coinbene
from exchange.bitz import bitz


class ex:

    list = [
        ('weidex', weidex.symbols.keys()),
        ('huobi', huobi.symbols.keys()),
        ('coinw', coinw.symbols.keys()),
        ('coinbene', coinbene.symbols.keys()),
        ('bitz', bitz.symbols.keys()),
    ]

    @staticmethod
    def get_balance(ex):
        if ex == 'weidex':
            return weidex.get_balance()
        elif ex == 'huobi':
            return huobi.get_balance()
        elif ex == 'coinw':
            return coinw.get_balance()
        elif ex == 'coinbene':
            return coinbene.get_balance()
        elif ex == 'bitz':
            return bitz.get_balance()
        return False


    @staticmethod
    def get_depth(ex, symbol, size = 1):
        if ex == 'weidex':
            return weidex.get_depth(symbol, size)
        elif ex == 'huobi':
            return huobi.get_depth(symbol, size)
        elif ex == 'coinw':
            return coinw.get_depth(symbol, size)
        elif ex == 'coinbene':
            return coinbene.get_depth(symbol, size)
        elif ex == 'bitz':
            return bitz.get_depth(symbol, size)
        return [{
            'buy_price': 0,
            'buy_amount': 0,
            'sell_price': 0,
            'sell_amount': 0,
        }]

    @staticmethod
    def get_fee(ex):
        if ex == 'weidex':
            return 0
        else:
            return 0.002

    @staticmethod
    def order(ex, type, symbol, price, amount):
        status = False
        if ex == 'weidex':
            status = weidex.order(type, symbol, price, amount)
        elif ex == 'huobi':
            status = huobi.order(type, symbol, price, amount)
        elif ex == 'coinw':
            status = coinw.order(type, symbol, price, amount)
        elif ex == 'coinbene':
            status = coinbene.order(type, symbol, price, amount)
        elif ex == 'bitz':
            status = bitz.order(type, symbol, price, amount)

        return status


if __name__ == '__main__':
    ex.get_depth('weidex', 'swtc/cnyt')
