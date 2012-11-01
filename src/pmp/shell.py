from __future__ import absolute_import

import subprocess
import sys


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


def sh(*args, **kwargs):
    # kwargs.setdefault('stdout', subprocess.PIPE)
    # kwargs.setdefault('stderr', sys.stderr)
    return subprocess.check_call(args, **kwargs)
