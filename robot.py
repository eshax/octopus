#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
机器人

根据策略配置执行交易动作

# 策略内容
1. 条件 (例如市场差价、是否达到最小搬砖量、是否账户有足够的资金、是否所搬币种存在余额等等)
2. 动作 (例如下单、提币、充币、提现、以及改变策略状态的动作等等)
"""

tactics = {
    "exchanges":[
        {"exchange": "weidex", "symbols": ["swtc/cnyt"]},
        {"exchange": "coinw", "symbols": ["swtc/cnyt"]}
    ],
    "rules": "depth['swtc/cnyt']['coinw']['sell_price'] > depth['swtc/cnyt']['weidex']['buy_price'] and depth['swtc/cnyt']['weidex']['buy_amount'] > 20000 and depth['swtc/cnyt']['coinw']['sell_amount'] > 20000",
    "actions":[
        { "sell.swtc/cnyt.coinw": 20000 },
        { "buy.swtc/cnyt.weidex": 20000 }
    ]
}

import os, sys, time, threading

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)

from octopus.market import depth, space, account

data = {}

def market():

    while True:

        for exchange in tactics['exchanges']:
            for symbol in exchange['symbols']:
                if symbol not in data:
                    data[symbol] = {}
                if exchange['exchange'] not in data[symbol]:
                    data[symbol][exchange['exchange']] = depth.get(exchange['exchange'], symbol)

        time.sleep(1)


def rule():

    rules = tactics['rules'].replace("depth", "data")

    while True:
        try:
            print(eval(rules))
        except:
            pass
        time.sleep(1)


threading.Thread(target=market, args=()).start()
threading.Thread(target=rule, args=()).start()
