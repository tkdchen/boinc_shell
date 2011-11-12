# -*- coding: utf-8 -*-

from sys import argv

class ARGV_VISITOR(object):
    def __init__(self):
        self._i = 0

    def next_argv(self):
        self._i += 1
        if self._i < len(argv):
            return argv[self._i]
        else:
            return None
