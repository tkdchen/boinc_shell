# -*- coding: utf-8 -*-

from xml.dom import Node
from xml.dom.minidom import parseString

class GUI_URL(object):
    def __init__(self):
        self.name        = ""
        self.description = ""
        self.url         = ""

    def parse(self, xmlnode):
        for item in xmlnode.childNodes:
            if item.nodeType == Node.ELEMENT_NODE:
                s = item.nodeName
                if s == "name":
                    self.name = item.firstChild.nodeValue; continue
                if s == "description":
                    self.description = item.firstChild.nodeValue; continue
                if s == "url":
                    self.url = item.firstChild.nodeValue; continue

    def show(self):
        print "name: %s\n" \
              "description: %s\n" \
              "url: %s\n" % (
                  self.name, self.description, self.url)

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_url(self):
        return self.url

class GUI_URLS(object):
    def __init__(self):
        self.gui_urls = []
        self.team = None

    def parse(self, xmlnode):
        for item in xmlnode.childNodes:
            if item.nodeType == Node.ELEMENT_NODE:
                if item.nodeName == "ifteam":
                    nd = item.firstChild
                    while nd != None and nd.nodeType != Node.ELEMENT_NODE:
                        nd = nd.nextSibling
                    self.team = GUI_URL()
                    self.team.parse(nd)
                else:
                    o = GUI_URL()
                    o.parse(item)
                    self.gui_urls.append(o)

    def show(self):
        for item in self.gui_urls:
            item.show()
        if self.team != None:
            self.team.show()

    def ifteam(self):
        return self.team != None

    def team(self):
        return self.team

    def get_gui_urls(self):
        return self.gui_urls

class GUIUrls(dict):

    def parse(self, xmlnode):
        for item in xmlnode.childNodes:
            if item.nodeType == Node.ELEMENT_NODE:
                if item.nodeName == "ifteam":
                    nd = item.firstChild
                    while nd != None and nd.nodeType != Node.ELEMENT_NODE:
                        nd = nd.nextSibling
                    self.team = GUI_URL()
                    self.team.parse(nd)
                else:
                    o = GUI_URL()
                    o.parse(item)
                    self[o.name] = o

    def list(self):
        pass
    show = list
