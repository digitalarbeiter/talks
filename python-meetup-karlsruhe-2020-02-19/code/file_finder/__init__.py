# coding: utf-8
# compat: py3
from __future__ import absolute_import

import logging
import os
import time

_log = logging.getLogger(__name__)


def file_finder(spooldir, subdirs, interval, errors):
    """
    Watch a spooldir structure for new files, move, and yield them.
    This will run indefinitely: if there are no files, the function will
    just sleep for the given interval before retrying.

    SIGTERM will cause an orderly shutdown but may take some time as
    file_finder will only react after the current file has been processed.
    This is necessary to allow for index consistency.

    Args:
        spooldir (str): The spool directory, e.g. /var/spool/searchqueue.
        subdirs (list): The subdirectories to watch, e.g. ["main", "queries", ...]
        interval (int): The number of seconds to wait between subsequent checks.
        errors (dict): The dictionary to log errors to.

    Yields:
        tuple: A tuple representing a file:
            queue (str): The subdirectory we got the file from
            path (str): Where the file is now
            delete (bool): Whether the file should be deleted after processing.
    """
    while True:
        new_files = []
        for subdir in subdirs:
            path = os.path.join(spooldir, subdir)
            for filename in os.listdir(os.path.join(path, "new")):
                new_files.append((path, filename, subdir))
        if any(filename == "pause" for _, filename, __ in new_files):
            errors["paused"] = True
            _log.warning("paused")
            time.sleep(interval)
            continue
        errors.pop("paused", None)
        for path, filename, queue in sorted(new_files):
            os.rename(
                os.path.join(path, "new", filename),
                os.path.join(path, "cur", filename),
            )
            yield queue, os.path.join(path, "cur", filename), True
        if not new_files:
            time.sleep(interval)
