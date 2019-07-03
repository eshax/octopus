#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_path)

from octopus.exchange.coinw import coinw
from octopus.exchange.weidex import weidex
from octopus.exchange.coinbene import coinbene

class exchange:

    '''
    交易所列表 以及交易所对象
    '''
    exchanges = {
        "coinw": coinw,
        "weidex": weidex,
        "coinbene": coinbene
    }

    '''
    全局币种列表
    交易所内的币种超出这个范围将被忽略
    '''
    symbols = [
        "swtc/cnyt",
    ]

    '''
    获取交易深度
    params::
            e: 交易所代码
            s: 币种
         size: 长度
    '''
    @staticmethod
    def get_depth(e, s, size = 1):

        if e not in exchange.exchanges:
            return False

        if s not in exchange.symbols:
            return False

        return exchange.exchanges[e].get_depth(s, size)

    '''
    下单
    params::
                e: 交易所代码
                t: 下单类型 (buy: 买 sell: 卖)
                s: 币种
                p: 下单价格
                a: 下单量
        apiconfig: API 参数
    '''
    @staticmethod
    def order(e, t, s, p, a, apiconfig = {}):

        if e not in exchange.exchanges:
            return False

        if s not in exchange.symbols:
            return False

        try:
            p = float(p)
            a = float(a)
            return exchange.exchanges[e].order(t, s, p, a, apiconfig)
        except:
            return False

    '''
    查询委托列表
    params::
                e: 交易所代码
        apiconfig: API 参数
    '''
    @staticmethod
    def orders(e, apiconfig = {}):

        return exchange.exchanges[e].orders(apiconfig)


if __name__ == '__main__':

    params = sys.argv

    if len(params) == 1:
        print()
        print("commend:")
        print(" depth  \t python exchange.py depth weidex swtc/cnyt")
        print(" order  \t python exchange.py order weidex buy swtc/cnyt 0.0060 10000")
        print(" orders \t python exchange.py orders weidex")
        print()

    if len(params) > 1:
        cmd = params[1]

        if cmd == "depth":
            if len(params) == 4:
                e, s = params[2:]
                print(exchange.get_depth(e, s))

        if cmd == "order":
            if len(params) == 7:
                e, t, s, p, a = params[2:]
                print(exchange.order(e, t, s, p, a))

        if cmd == "orders":
            if len(params) == 3:
                e = params[2]
                print(exchange.orders(e))
