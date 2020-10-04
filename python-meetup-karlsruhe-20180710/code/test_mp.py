# -*- coding: utf-8 -*-
#
# run with: py.test --cov . --cov-report=html -s test_mp.py

import os
import sys
import multiprocessing

def print_val(val):
    print "[pid:%s].print_val(%r)" % (os.getpid(), val)

def _test_mp():
    print ""
    print "[pid:%i].test_mp()" % os.getpid()
    p = multiprocessing.Process(target=print_val, args=("unittest mp",))
    p.start()
    p.join()
    assert p.exitcode == 0

def test_fork():
    print ""
    print "[pid:%i].test_fork()" % os.getpid()
    pid = os.fork()
    if pid == 0:
        print_val("unittest fork")
        os._exit(0)
    else:
        child_pid, exitcode = os.waitpid(pid, 0)
        assert child_pid == pid
        assert os.WEXITSTATUS(exitcode) == 0
