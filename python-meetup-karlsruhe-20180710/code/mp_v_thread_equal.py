#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import multiprocessing

def print_val(val):
    print val

if __name__ == "__main__":
    t = threading.Thread(
        target=print_val,
        args=("hi from thread",),
    )
    t.start()
    t.join()

    p = multiprocessing.Process(
        target=print_val,
        args=("hi from process",),
    )
    p.start()
    p.join()

