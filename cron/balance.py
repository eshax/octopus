#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import logging

logging.getLogger("urllib3").setLevel(logging.WARNING)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db import db
from utils.ex import ex

for exchange, _ in ex.list:
    balance = ex.get_balance(exchange)
    if balance:
        for item in balance:
            if item != 'exchange':
                db.redis.hset('balance.' + exchange, item.lower(), balance[item])

    
