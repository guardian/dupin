from __future__ import print_function

import sys


def printerr(*args, **kwargs):
    kwargs["file"] = sys.stderr
    print(*args, **kwargs)
