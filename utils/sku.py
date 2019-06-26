#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.db import db
from utils.ex import ex
from cron.otc import otc


class sku:

    @staticmethod
    def reset(exchange, symbol):
        db.redis.delete('sku.%s.%s' % (exchange, symbol.split('/')[0]))

    @staticmethod
    def buy(exchange, symbol, price, amount):
        status = ex.order(exchange, 'buy', symbol, price, amount)
        return status

    @staticmethod
    def sell(exchange, symbol, price, amount):
        status = ex.order(exchange, 'sell', symbol, price, amount)
        return status


if __name__ == '__main__':
    pass
