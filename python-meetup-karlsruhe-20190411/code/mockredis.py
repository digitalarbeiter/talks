# -*- coding: utf-8 -*-
# mock redis

import random
import time

_cache = {}


t_roundtrip = 0.005
t_upper = 0.010

def dbsize():
    time.sleep(t_roundtrip)
    return len(_cache)

def get(key):
    time.sleep(t_roundtrip)
    if key in _cache:
        time.sleep(t_upper * random.random())
    return _cache.get(key, None)

def setex(key, data, _expire):
    time.sleep(t_roundtrip)
    time.sleep(t_upper * random.random())
    _cache[key] = data
