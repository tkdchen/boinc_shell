# -*- coding: utf-8 -*-

from core import *

bsc = None

try:
    bsc = shell_core()
    bsc.prepare()
    if bsc.authorized():
        projects = bsc.get_project_status()
        for project in projects.projects:
            print
            print "name: %s\n" \
                  "url: %s" % (project.project_name, project.master_url)
finally:
    if bsc != None:
        bsc.done()
