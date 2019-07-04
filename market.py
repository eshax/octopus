#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import threading
import time
import memcache
import json

mc = memcache.Client(['127.0.0.1:11211'], debug=True)

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)

from octopus.exchange.exchange import exchange as ex

'''
全局设置
'''
def set_config(conf_path):

    try:

        with open(conf_path, 'r') as f:
            cf = json.load(f)

            for c in ['symbols', 'apiconfig']:
                if c not in cf:
                    print("config no %s!" % c)
                    return False

            '''
            全局币种设置
            适用于交易所内币种是否设置准确的检测
            '''
            ex.symbols = cf.get("symbols").get("global", [])

            for e in ex.exchanges:

                '''
                交易所内币种设置
                超出全局币种设置的将被忽略 不会进行深度及空间的检测 更不会进行搬砖
                '''
                ex.exchanges[e].symbols = cf.get("symbols").get(e, {})

                '''
                交易所基础API设置
                仅用于市场深度以及空间的检测, 不适用于搬砖
                搬砖所使用的 API 需要在 robot 的策略配置中传入
                '''
                ex.exchanges[e].apiconfig = cf.get("apiconfig").get(e, {})

        return True

    except Exception as e:
        print(e)
        return False

"""
市场深度
1. 实时查询各个交易所各个币种的挂单价格
2. 将挂单数据存储在 memcache 数据库中、数据存活期为 5 秒钟
3. 提供某个市场某个币种交易深度的订阅接口
"""
class depth:

    @staticmethod
    def run():
        for e in ex.exchanges:
            for s in ex.exchanges[e].symbols:
                if s in ex.symbols:
                    threading.Thread(target=depth.scan, args=(e, s)).start()

    @staticmethod
    def scan(e, s):
        k = '%s.%s' % (e, s)
        while True:
            o = ex.get_depth(e, s)
            if o:
                o = o[0]
                bp, sp = float(o.get("buy_price")), float(o.get("sell_price"))
                if bp > 0 and sp > 0:
                    mc.set(k, o, 20)
                    # print(e, s, mc.get(k))
            time.sleep(10)

    @staticmethod
    def get(e, s):
        k = '%s.%s' % (e, s)
        return mc.get(k)

"""
市场空间
1. 根据市场深度提供的报价数据、监控同币种在不同市场上的差价
2. 将差价数据存放到实时数据库中、数据存活期为 5 秒钟
3. 提供某两个市场某个币种差价订阅接口
"""
class space:

    @staticmethod
    def run():

        # Cross Exchange Bilateral Trade
        data = [(e, set(ex.exchanges[e].symbols.keys())) for e in ex.exchanges]
        data = [(e1, e2, s1, s2) for e1, s1 in data for e2, s2 in data if e2 > e1]
        for e1, e2, s1, s2 in data:
            for s in (s1 & s2):
                threading.Thread(target=space.cebt, args=(e1, e2, s)).start()

    @staticmethod
    def cebt(e1, e2, s):

        while True:
            d1 = depth.get(e1, s)
            d2 = depth.get(e2, s)
            if d1 and d2:
                for e1, e2, d1, d2 in [(e1, e2, d1, d2), (e2, e1, d2, d1)]:
                    p1, p2, a1, a2 = float(d1.get("buy_price")), float(d2.get("sell_price")), float(d1.get("buy_amount")), float(d2.get("sell_amount"))
                    k = '%s.%s.%s' % (e1, e2, s)
                    o = {
                        "from" : e1,
                        "to" : e2,
                        "symbol" : s,
                        "buy_price": p1,
                        "buy_amount": a1,
                        "sell_price": p2,
                        "sell_amount": a2,
                        "amount": min(a1, a2),
                        "space": p2 - p1,
                        "ratio": (p2 - p1) / min(p1, p2),
                    }
                    mc.set(k, o, 4)
                    x = mc.get(k)
                    print(time.strftime("%Y-%m-%d %H:%M:%S"), {
                        "from": x['from'],
                        "to": x['to'],
                        "symbol": x['symbol'],
                        "space": round(x['space'], 6),
                        "ratio": round(x['ratio'], 4),
                    })
            time.sleep(2)

"""
账户
1. 根据 api_key 监控交易所的账户状态
2. 将账户中各种币的余额存放在数据库中
3. 提供某个市场某个账户信息的订阅接口
"""
class account:

    pass


if __name__ == '__main__':

    if len(sys.argv) > 1:
        '''
        usage:
            python market.py octopus.conf
        '''
        if not set_config(sys.argv[1]):
            print('config error!')
            exit()

    set_config("octopus.conf")

    depth.run()

    space.run()
