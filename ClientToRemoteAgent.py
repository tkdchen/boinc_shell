# -*- coding: utf-8 -*-

from rpc_call import GET_PROJECT_STATUS, GET_RESULTS
from project import PROJECTS
from result import RESULTS
from socket import *
from sys import argv
from xml.dom.minidom import parseString
from cStringIO import StringIO

class RemoteAgentInfo(object):
    def __init__(self, machine_name, port):
        self.machine_name = machine_name
        self.port = port
    def getMachineName(self):
        return self.machine_name
    def getPort(self):
        return self.port

agentList = []

def load_agent_entities(config_file):
    import os.path
    col = []
    fh = open(config_file)
    xmldoc = parse(fh)
    node = xmldoc.documentElement.firstChild
    while node != None:
        if node.nodeType == Node.ELEMENT_NODE:
            ae = AgentEntity()
            ae.name = node.getAttribute("name")
            ae.ip = node.getAttribute("ip")
            ae.port = int(node.getAttribute("port"))
            col.append(ae)
        node = node.nextSibling
    fh.close()
    return col

def read_socket(sock):
    buffersize = 4096
    buf = StringIO()

    while True:
        s = sock.recv(buffersize)
        buf.write(s)
        if len(s) < buffersize:
            break

    s = buf.getvalue()
    buf.close()
    return s

def read_config():
    f = open("ClientToRemoteAgent.config", "r+")
    s = f.readline()
    while s:
        pos = s.find(",")
        agentList.append(RemoteAgentInfo(s[0:pos],int(s[pos+1:])))
        s = f.readline()
    f.close()

def get_projects_count(client):
    client.send(GET_PROJECT_STATUS)
    xmldoc = parseString(read_socket(client))
    return len(xmldoc.getElementsByTagName("project"))

def get_results_count(client):
    client.send(GET_RESULTS)
    xmldoc = parseString(read_socket(client))
    return len(xmldoc.getElementsByTagName("result"))

def get_projects(client):
    client.send(GET_PROJECT_STATUS)
    xmldoc = parseString(read_socket(client))
    ps = PROJECTS()
    ps.parse(xmldoc.documentElement)
    return ps

def get_results(client):
    client.send(GET_RESULTS)
    xmldoc = parseString(read_socket(client))
    rs = RESULTS()
    rs.parse(xmldoc.documentElement)
    return rs

def get_file_transfers(client):
    pass

def server_status_view():
    client = socket(AF_INET, SOCK_STREAM)
    # visit each remote agent and display its status
    for agentinfo in agentList:
        try:
            client.connect((gethostbyname(agentinfo.getMachineName()), agentinfo.getPort()))
            status = None
            if read_socket(client) == "<server_ok/>":
                status = "running"
            else:
                status = "down"
            print "%s: %s; Projects(%d); Results(%d)" % (
                agentinfo.getMachineName(), status,
                get_projects_count(client),
                get_results_count(client))
            client.shutdown(SHUT_RDWR)
            client.close()
        except:
            print "%s service: down\n" % (agentinfo.getMachineName())
    client = None

if __name__ == "__main__":
    read_config()

    server_status_view()
