#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib

class md5:

    '''
    md5 加密
    '''
    @staticmethod
    def encode(str):
        m1 = hashlib.md5()
        m1.update(str.encode('utf-8'))
        token = m1.hexdigest()
        return token

