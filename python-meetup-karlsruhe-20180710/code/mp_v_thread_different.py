#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import multiprocessing

def append_val(lst, val):
    lst.append(val)

if __name__ == "__main__":
    l = []
    t = threading.Thread(
        target=append_val,
        args=(l, "hi from thread",),
    )
    t.start()
    t.join()
    print "list after thread:", l

    l = []
    p = multiprocessing.Process(
        target=append_val,
        args=(l, "hi from process",),
    )
    p.start()
    p.join()
    print "list after process:", l

