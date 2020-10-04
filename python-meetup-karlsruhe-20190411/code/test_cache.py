#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time

from cache import cache_when_worth_it

def my_key(args, kwargs):
    return "{!r}.{!r}.{!r}".format(*args)

@cache_when_worth_it(my_key, average_over=3)
def my_func(a, b, c):
    print("not cached: my_func({}, {}, {})".format(a, b, c))
    start = time.monotonic()
    result = 0.0
    for x in range(a):
        for y in range(b):
            for z in range(c):
                result += x*y*z
    print("    computation time: {:.3f}s".format(time.monotonic()-start))
    return result

def run():
    print("calibration...")
    calibration = 20 * [(1, 1, 1)]
    for a, b, c in calibration:
        my_func(a, b, c)
    print("calibration finished, overhead: {:.3f}".format(my_func.cache.overhead))
    print("")
    data = [
        (5, 5, 5),
        (10, 10, 10),
        (15, 15, 15),
        (50, 50, 50),
        (200, 100, 100),
        (200, 500, 500),
        (5, 5, 5),
        (10, 10, 10),
        (15, 15, 15),
        (50, 50, 50),
        (200, 100, 100),
        (200, 500, 500),
    ]
    for a, b, c in data:
        print("{}x{}x{}".format(a, b, c))
        start = time.monotonic()
        res = my_func(a, b, c)
        print("{}x{}x{}={} (took {:.3f}s)".format(a, b, c, res, time.monotonic()-start))
        print("")

if __name__ == "__main__":
    run()
