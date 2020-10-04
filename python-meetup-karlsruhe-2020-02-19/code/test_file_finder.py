# coding: utf-8
# compat: py3
from __future__ import absolute_import

import os
import threading
import time

from file_finder import file_finder


def _mkspool(tmpdir, indices, n_files=1):
    for idx in indices:
        tmpdir.mkdir(idx)
        tmpdir.mkdir(idx+"/new")
        tmpdir.mkdir(idx+"/cur")
    files = [
        "{}/{}/new/{:03}_delta.jdiff".format(str(tmpdir), idx, cnt)
        for idx in indices
        for cnt in range(n_files)
    ]
    return files


def test_file_finder(tmpdir):
    indices = ["main", "shopsonline"]
    files = _mkspool(tmpdir, indices, n_files=10)
    errors = {}
    finder = file_finder(str(tmpdir), indices, interval=2, errors=errors)
    for fname in files:
        with open(fname, "w") as f:
            f.write(fname)
        index, found, to_delete = next(finder)
        assert found == fname.replace("/new/", "/cur/")
        assert index in found
        assert index in indices
        assert to_delete
    assert not errors


def test_file_finder_empty_filled(tmpdir):
    indices = ["empty"]
    _mkspool(tmpdir, indices, n_files=0)

    def _create_file():
        time.sleep(3.1)
        with open("{}/{}/new/{}".format(str(tmpdir), indices[0], "000_delta.json"), "w") as f:
            f.write("le wilde data appears")

    creator = threading.Thread(target=_create_file, args=[])
    creator.start()
    errors = {}
    finder = file_finder(str(tmpdir), indices, interval=2, errors=errors)
    started = time.monotonic()
    index, found, to_delete = next(finder)
    appeared = time.monotonic()
    creator.join()
    assert time.monotonic() - appeared < 0.1  # creator thread should be long done
    assert appeared - started >= 3
    assert index in found
    assert to_delete
    assert not errors
    assert open(found, "r").read() == "le wilde data appears"


def test_file_finder_pause(tmpdir):
    indices = ["p_a_u_s_e"]
    _mkspool(tmpdir, indices, n_files=0)
    errors = {}
    interval = 1.0

    def _pause_come_and_go():
        time.sleep(0.5*interval)
        pause_file = "{}/{}/new/pause".format(str(tmpdir), indices[0])
        with open(pause_file, "w") as f:
            f.write("le wilde pause appears")
        time.sleep(1.5*interval)
        assert "paused" in errors
        os.remove(pause_file)
        time.sleep(1.5*interval)
        assert "paused" not in errors
        with open("{}/{}/new/{}".format(str(tmpdir), indices[0], "000_delta.json"), "w") as f:
            f.write("le wilde data appears")

    creator = threading.Thread(target=_pause_come_and_go, args=[])
    creator.start()
    finder = file_finder(str(tmpdir), indices, interval=interval, errors=errors)
    started = time.monotonic()
    index, found, to_delete = next(finder)
    appeared = time.monotonic()
    creator.join()
    assert time.monotonic() - appeared < 0.1  # creator thread should be long done
    assert appeared - started >= 3.5*interval
    assert index in found
    assert to_delete
    assert not errors
    assert open(found, "r").read() == "le wilde data appears"
