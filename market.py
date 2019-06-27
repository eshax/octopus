#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import threading
import time
import memcache
import configparser

mc = memcache.Client(['127.0.0.1:11211'], debug=True)

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)

from octopus.exchange.exchange import exchange as ex

'''
全局设置
'''
def set_config(conf_path):

    try:
        cf = configparser.ConfigParser()
        cf.read(conf_path, encoding='utf-8')

        '''
        全局币种设置
        适用于交易所内币种是否设置准确的检测
        '''
        symbols = []
        for opt in cf.options('symbols'):
            for symbol in cf.get('symbols', opt).split(','):
                symbols.append("%s_%s" % (symbol, opt))
        ex.symbols = symbols

        '''
        交易所内币种设置
        超出全局币种设置的将被忽略 不会进行深度及空间的检测 更不会进行搬砖
        '''
        for st in cf.sections():
            data = {}
            if '.symbols' in st:
                e = st.split('.')[0]
                for opt in cf.options(st):
                    data[opt] = cf.get(st, opt)
                ex.exchanges[e].symbols = data

        '''
        交易所基础API设置
        仅用于市场深度以及空间的检测, 不适用于搬砖
        搬砖所使用的 API 需要在 robot 的策略配置中传入
        '''
        for st in cf.sections():
            data = {}
            if '.apiconfig' in st:
                e = st.split('.')[0]
                for opt in cf.options(st):
                    data[opt] = cf.get(st, opt)
                ex.exchanges[e].apiconfig = data


        return True

    except:
        return False

"""
市场深度
1. 实时查询各个交易所各个币种的挂单价格
2. 将挂单数据存储在 memcache 数据库中、数据存活期为 3 秒钟
3. 提供某个市场某个币种交易深度的订阅接口
"""
class depth:

    @staticmethod
    def run():
        for e in ex.exchanges:
            for s in ex.exchanges[e].symbols:
                if s in ex.symbols:
                    threading.Thread(target=depth.get, args=(e, s)).start()

    @staticmethod
    def get(e, s):
        while True:
            o = ex.get_depth(e, s)
            if o:
                mc.set(e + s, o, 5)
                print(e, s, mc.get(e + s))
            time.sleep(5)

"""
市场空间
1. 根据市场深度提供的报价数据、监控同币种在不同市场上的差价
2. 将差价数据存放到实时数据库中、数据存活期为 5 秒钟
3. 提供某两个市场某个币种差价订阅接口
"""
class space:

    pass


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

    depth.run()
