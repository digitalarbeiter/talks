#!/usr/bin/env python3
# coding: utf-8
# compat: py3
from __future__ import absolute_import


def get_exports():
    # for some complicated reason, we cannot join "seen" to the exports here
    return [
        {"id": ex_id, "filename": "export_{:03}.json".format(ex_id)}
        for ex_id in range(10)
    ]


def is_export_seen(ex_id):
    return {
        0: True,
        1: True,
        2: True,
        3: True,
        4: True,
        5: False,
        6: True,
        7: False,
        8: True,
        9: False,
    }[ex_id]


def handle_unseen_exports():
    exports = get_exports()
    print("all exports: {}".format(exports))
    seen_exports = (ex["id"] for ex in exports if is_export_seen(ex["id"]))
    # ...
    for ex in exports:
        if ex["id"] in seen_exports:
            print("skipping seen export {}".format(ex))
            continue
        print("handling unseen export {}...".format(ex))
        if is_export_seen(ex["id"]):
            print("this should never happen")


if __name__ == "__main__":
    handle_unseen_exports()
