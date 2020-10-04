# coding: utf-8
# compat: py3
from __future__ import absolute_import

import json

def jsonreader(it):
    for line in it:
        yield json.loads(line)
