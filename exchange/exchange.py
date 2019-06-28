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
            s: 币种
            p: 下单价格
            a: 下单量
    apiconfig: API 参数
    '''
    @staticmethod
    def order(e, s, p, a, apiconfig = {}):
        pass


if __name__ == '__main__':

    print(exchange.get_depth("coinw", "swtc/cnyt"))
    print(exchange.get_depth("huobi", "swtc/cnyt"))
