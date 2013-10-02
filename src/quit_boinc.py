# -*- coding: utf-8 -*-

from core import *

bsc = None

try:
    bsc = shell_core()
    bsc.prepare()
    if bsc.authorized():
        bsc.quit_boinc()
finally:
    if bsc != None:
        bsc.done()
