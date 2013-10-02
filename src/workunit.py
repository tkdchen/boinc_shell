# -*- coding: utf-8 -*-

from xml.dom import parseString
from xml.dom.minidom import Node

class WORKUNIT(object):
    def __init__(self):
        self.name             = ""
        self.app_name         = ""
        self.version_num      = 0
        self.rsc_fpops_est    = 0.0
        self.rsc_fpops_bound  = 0.0
        self.rsc_memory_bound = 0.0
        self.rsc_disk_bound   = 0.0

        self.project = None # references an instance of class PROJECT
        self.app = None # references an instance of class APP
        self.avp = None # references an instance of class APP_VERSION

    def parse(self, source):
        pass

    def show(self):
        pass

class WORKUNITS(object):
    def __init__(self):
        self.workunits = []

    def parse(self, xmlnode):
        pass

    def show(self):
        pass

class WorkUnits(dict):

    def parse(self, xmlnode):
        pass

    def list(self):
        pass
    show = list
