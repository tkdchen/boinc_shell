# -*- coding: utf-8 -*-

from xml.dom.minidom import Node

class RESULT(object):
    def __init__(self):
        self.name                = ""
        self.wu_name             = ""
        self.project_url         = ""
        self.report_deadline     = 0.0
        self.ready_to_report     = False
        self.got_server_ack      = False
        self.final_cpu_time      = 0.0
        self.state               = 0
        self.scheduler_state     = 0
        self.exit_status         = 0
        self.signal              = 0
        self.stderr_out          = ""
        self.suspended_via_gui   = False
        self.aborted_via_gui     = False

        # the folowng defined if active
        self.active_task         = False
        self.active_task_state   = 0
        self.app_version_num     = 0
        self.checkpoint_cpu_time = 0.0
        self.current_cpu_time    = 0.0
        self.fraction_done       = 0.0
        self.vm_bytes            = 0.0
        self.rss_bytes           = 0.0
        self.estimated_cpu_time_remaining = 0.0
        self.supports_graphics   = False
        self.graphics_mode_acked = 0
        self.app                 = None # references an instance of class APP
        self.wup                 = None # references an instance of class WORKUNIT
        self.project             = None # references an instance of class PROJECT

    def is_active(self):
        return self.active_task

    def parse(self, node):
        for item in node.childNodes:
            if item.nodeType == Node.ELEMENT_NODE:
                nn = item.nodeName
                if nn == "name":
                    self.name = item.firstChild.nodeValue
                elif nn == "wu_name":
                    self.wu_name = item.firstChild.nodeValue
                elif nn == "project_url":
                    self.project_url = item.firstChild.nodeValue
                elif nn == "report_deadline":
                    self.report_deadline = float(item.firstChild.nodeValue)
                elif nn == "final_cpu_time":
                    self.final_cpu_time = float(item.firstChild.nodeValue)
                elif nn == "exit_status":
                    self.exit_status = int(item.firstChild.nodeValue)
                elif nn == "state":
                    self.state = int(item.firstChild.nodeValue)
                elif nn == "estimated_cpu_time_remaining":
                    self.estimated_cpu_time_remaining = float(item.firstChild.nodeValue)
                elif nn == "ready_to_report":
                    self.ready_to_report = True
                elif nn == "active_task":
                    self.active_task = True
                    for ati in item.childNodes:
                        if ati.nodeType == Node.ELEMENT_NODE:
                            nn = ati.nodeName
                            if nn == "active_task_state":
                                self.project_master_url = int(ati.firstChild.nodeValue)
                            elif nn == "app_version_num":
                                self.app_version_num = int(ati.firstChild.nodeValue)
                            elif nn == "scheduler_state":
                                self.scheduler_state = int(ati.firstChild.nodeValue)
                            elif nn == "checkpoint_cpu_time":
                                self.checkpoint_cpu_time = float(ati.firstChild.nodeValue)
                            elif nn == "fraction_done":
                                self.fraction_done = float(ati.firstChild.nodeValue)
                            elif nn == "current_cpu_time":
                                self.current_cpu_time = float(ati.firstChild.nodeValue)
                            elif nn == "vm_bytes":
                                self.vm_bytes = float(ati.firstChild.nodeValue)
                            elif nn == "rss_bytes":
                                self.rss_bytes = float(ati.firstChild.nodeValue)
                            elif nn == "supports_graphics":
                                self.supports_graphics = True
                            elif nn == "graphics_mode_acked":
                                self.graphics_mode_acked = int(ati.firstChild.nodeValue)

    def show(self):
        print "name: %s\n" \
              "wu_name: %s\n" \
              "fraction_done: %s" % (self.name, self.wu_name, self.fraction_done)

class RESULTS(object):
    def __init__(self):
        self.results = []

    def results(self):
        return self.results

    def parse(self, node):
        for item in node.childNodes:
            if item.nodeType == Node.ELEMENT_NODE and item.nodeName == "results":
                for resultNode in item.childNodes:
                    if resultNode.nodeType == Node.ELEMENT_NODE:
                        result = RESULT()
                        result.parse(resultNode)
                        self.results.append(result)

    def getCount(self):
        return len(self.results)

    def show(self):
        for result in self.results:
            result.show()

    def lookup_result(self, name):
        for r in self.results:
            if r.name == name:
                return r
        return None

class Results(dict):

    def parse(self, node):
        for item in node.childNodes:
            if item.nodeType == Node.ELEMENT_NODE and item.nodeName == "results":
                for resultNode in item.childNodes:
                    if resultNode.nodeType == Node.ELEMENT_NODE:
                        result = RESULT()
                        result.parse(resultNode)
                        self[result.wu_name] = result

    def list(self):
        for key, val in self:
            val.show()
    show = list
