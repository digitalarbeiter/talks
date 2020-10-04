# -*- coding: utf-8 -*-

import json
import random
import time
from hashlib import sha1
from collections import deque
from functools import wraps

import mockredis as redis


class MovingAverage:
    def __init__(self, n):
        self.deque = deque(0 for _ in range(n))
        self.sum = 0
        self.n = n

    def push(self, item):
        self.sum -= self.deque.popleft()
        self.deque.append(item)
        self.sum += item

    @property
    def value(self):
        return self.sum / self.n


class CacheProxy:
    def __init__(self, cache_time=600, hard_cache_size_limit=50000, average_over=1000):
        self.cache_time = cache_time
        self.hard_cache_size_limit = hard_cache_size_limit
        self.moving_avg = MovingAverage(average_over)

    @property
    def overhead(self):
        return self.moving_avg.value

    def _get_key(self, key_data):
        return sha1(key_data.encode("utf-8")).hexdigest()

    def __getitem__(self, key_data):
        start = time.monotonic()
        key = self._get_key(key_data)
        result = redis.get(key)
        if result:
            result = json.loads(result)
            self.moving_avg.push(time.monotonic() - start)
            return result
        else:
            if random.random() > 0.99:
                self.moving_avg.push(0)
            raise KeyError

    def __setitem__(self, key_data, result):
        key = self._get_key(key_data)
        cache_size = redis.dbsize()
        if cache_size < self.hard_cache_size_limit:
            redis.setex(key, json.dumps(result), int(self.cache_time))


def cache_when_worth_it(cache_key_generator, *cache_args, **cache_kwargs):
    def decorator(fn):
        fn.cache = CacheProxy(*cache_args, **cache_kwargs)

        @wraps(fn)
        def wrapper(*args, **kwargs):
            key_data = cache_key_generator(args, kwargs)
            try:
                return fn.cache[key_data]
            except KeyError:
                start = time.monotonic()
                result = fn(*args, **kwargs)
                if key_data and time.monotonic() - start > fn.cache.overhead:
                    fn.cache[key_data] = result
                return result

        return wrapper

    return decorator
