#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
import mysql.connector.pooling

class db:
    redis = redis.Redis(host='127.0.0.1', port=6379, db=2, decode_responses=True)

    __mysql_config = {
        'user': 'root',
        'password': 'Trading123!@#',
        'host': '127.0.0.1',
        'database': 'trading'
    }

    mysql = mysql.connector.pooling.MySQLConnectionPool(pool_name='dbpool', pool_size=5, pool_reset_session=True, **__mysql_config)
