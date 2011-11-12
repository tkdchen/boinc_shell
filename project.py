# -*- coding: utf-8 -*-

from xml.dom.minidom import *
from xml.dom import Node
from gui_url import GUI_URLS

class DAILY_STATS(object):
    def __init__(self):
        self.user_total_credit  = 0.0
        self.user_expavg_credit = 0.0
        self.host_total_credit  = 0.0
        self.host_expavg_credit = 0.0
        self.day = 0.0

    def parse(self, source):
        pass

    def show(self):
        print "user total credit: %f\n" \
              "user expavg credit: %f\n" \
              "host total credit: %f\n" \
              "host expavg credit: %f\n" \
              "day: %f\n" % (
                  self.user_total_credit,
                  self.user_expavg_credit,
                  self.host_total_credit,
                  self.host_expavg_credit,
                  self.day)

class PROJECT(object):
    def __init__(self):
        self.master_url = ""
        self.resource_share = 0.0
        self.project_name = ""
        self.user_name = ""
        self.team_name = ""
        self.gui_urls = GUI_URLS()
        self.user_total_credit  = 0.0
        self.user_expavg_credit = 0.0
        self.host_total_credit  = 0.0
        self.host_expavg_credit = 0.0
        self.disk_usage = 0.0
        self.nrpc_failures = 0
        self.master_fetch_failures = 0
        self.min_rpc_time = 0.0
        self.master_url_fetch_pending = False
        self.sched_rpc_pending = False
        self.tentative = False
        self.non_cpu_intensive = False
        self.suspended_via_gui = False
        self.dont_request_more_work = False
        self.statistics = [] # type of DAILY_STATS

    def parse(self, xmlnode):
        items = xmlnode.childNodes
        for item in items:
            if item.nodeType == Node.ELEMENT_NODE:
                name = item.nodeName

                if name == "master_url":
                    self.master_url = item.firstChild.nodeValue
                elif name == "resource_share":
                    self.resource_share = item.firstChild.nodeValue
                elif name == "project_name":
                    self.project_name = item.firstChild.nodeValue
                elif name == "user_name":
                    self.user_name = item.firstChild.nodeValue
                elif name == "team_name":
                    self.team_name = item.firstChild.nodeValue
                elif name == "user_total_credit":
                    self.user_total_credit = float(item.firstChild.nodeValue)
                elif name == "user_expavg_credit":
                    self.user_expavg_credit = float(item.firstChild.nodeValue)
                elif name == "host_total_credit":
                    self.host_total_credit = float(item.firstChild.nodeValue)
                elif name == "host_expavg_credit":
                    self.host_expavg_credit = float(item.firstChild.nodeValue)
                elif name == "":
                    self.disk_usage = float(item.firstChild.nodeValue)
                elif name == "nrpc_failures":
                    self.nrpc_failures = int(item.firstChild.nodeValue)
                elif name == "master_fetch_failures":
                    self.master_fetch_failures = int(item.firstChild.nodeValue) > 0
                elif name == "min_rpc_time":
                    self.min_rpc_time = float(item.firstChild.nodeValue)
                elif name == "master_url_fetch_pending":
                    self.master_url_fetch_pending = True
                elif name == "sched_rpc_pending":
                    self.sched_rpc_pending = True
                elif name == "non_cpu_intensive":
                    self.non_cpu_intersive = True
                elif name == "suspended_via_gui":
                    self.suspended_via_gui = True
                elif name == "dont_request_more_work":
                    self.dont_request_more_work = True
                elif name == "gui_urls":
                    self.gui_urls.parse(item)

    def show(self):
        print "------ %s ------" % (self.project_name)
        print "project url: %s\n"        \
              "user name: %s\n"          \
              "team name: %s\n"          \
              "user total credit: %f\n"  \
              "user expavg credit: %f\n" \
              "host total credit: %f\n"  \
              "host expavg credit: %f\n" \
              "disk usage: %f" % (
                  self.master_url,
                  self.user_name,
                  self.team_name,
                  self.user_total_credit,
                  self.user_expavg_credit,
                  self.host_total_credit,
                  self.host_expavg_credit,
                  self.disk_usage)

        self.gui_urls.show()


class PROJECTS(object):
    def __init__(self):
        self.projects = []

    def parse(self, xmlnode):
        project_nodes = xmlnode.childNodes
        for item in project_nodes:
            if item.nodeType == Node.ELEMENT_NODE and item.nodeName == "projects":
                for projnode in item.childNodes:
                    if projnode.nodeType == Node.ELEMENT_NODE:
                        p = PROJECT()
                        p.parse(projnode)
                        self.projects.append(p)

                break

    def getCount(self):
        return len(self.projects)

    def show(self):
        for p in self.projects:
            p.show()

    def lookup_project(self, project_name):
        for p in self.projects:
            if p.project_name == project_name:
                return p
        return None

class Projects(dict):

    def parse(self, xmlnode):
        project_nodes = xmlnode.childNodes
        for item in project_nodes:
            if item.nodeType == Node.ELEMENT_NODE and item.nodeName == "projects":
                for projnode in item.childNodes:
                    if projnode.nodeType == Node.ELEMENT_NODE:
                        p = PROJECT()
                        p.parse(projnode)
                        self[p.project_name] = p

    def list(self):
        for key, val in self:
            val.show()
    show = list
