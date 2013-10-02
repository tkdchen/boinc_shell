# -*- coding: utf-8 -*-

from xml.dom import Node

class APP_VERSION(object):
    def __init__(self):
        self.app_name    = ""
        self.version_num = 0
        self.app         = None # references an instance of class APP
        self.project     = None # references an instance of class PROJECT

    def parse(self, source):
        pass

    def show(self):
        pass
