# -*- coding: utf-8 -*-

from xml.dom import Node
from xml.dom.minidom import parseString
from httplib import HTTPConnection
import getopt
import sys
import urllib

user_info = None

class UserInfo(object):
    def __init__(self):
        self.id = ""
        self.cpid = ""
        self.create_time = ""
        self.name = ""
        self.country = ""
        self.total_credit = 0.0
        self.expavg_credit = 0.0
        self.teamid = ""
        self.url = ""
        self.has_profile = 0
        self.hosts = []

    def Parse(self, node):
        for item in node.childNodes:
            if item.nodeType == Node.ELEMENT_NODE:
                tagname = item.nodeName
                if tagname == "host":
                    host_info = HostInfo()
                    host_info.Parse(item)
                    self.hosts.append(host_info)
                else:
                    if len(item.childNodes) == 0:
                        tv = ""
                    else:
                        tv = item.firstChild.nodeValue
                    if tagname == "id":
                        self.id = tv
                    elif tagname == "cpid":
                        self.cpid = tv
                    elif tagname == "create_time":
                        self.create_time = tv
                    elif tagname == "name":
                        self.name = tv
                    elif tagname == "country":
                        self.country = tv
                    elif tagname == "total_credit":
                        self.total_credit = float(tv)
                    elif tagname == "expavg_credit":
                        self.expavg_credit = float(tv)
                    elif tagname == "teamid":
                        self.teamid = tv
                    elif tagname == "url":
                        self.url = tv
                    elif tagname == "has_profile":
                        self.has_profile = int(tv)

    def Show(self, show_hosts=False):
        print "           id: %s\n" \
              "         cpid: %s\n" \
              "  create time: %s\n" \
              "         name: %s\n" \
              "      country: %s\n" \
              " TOTAL CREDIT: %f\n" \
              "EXPAVG CREDIT: %f\n" \
              "       teamid: %s\n" \
              "          url: %s\n" \
              "  has_profile: %d\n" % (
                  self.id,
                  self.cpid,
                  self.create_time,
                  self.name,
                  self.country,
                  self.total_credit,
                  self.expavg_credit,
                  self.teamid,
                  self.url,
                  self.has_profile)

        if show_hosts:
            for o in self.hosts:
                o.Show()

class HostInfo(object):
    def __init__(self):
        self.id = ""
        self.create_time = ""
        self.rpc_seqno = ""
        self.host_cpid = ""
        self.total_credit = 0.0
        self.expavg_credt = 0.0
        self.domain_name = ""
        self.p_ncpus = 0
        self.p_vendor = ""
        self.p_fpops = 0.0
        self.p_iops = 0.0
        self.os_name = ""
        self.os_version = ""

    def Parse(self, node):
        for item in node.childNodes:
            if item.nodeType == Node.ELEMENT_NODE:
                tn = item.nodeName
                if len(item.childNodes) == 0:
                    tv = ""
                else:
                    tv = item.firstChild.nodeValue
                if tn == "id":
                    self.id = tv
                elif tn == "create_time":
                    self.create_time = tv
                elif tn == "rpc_seqno":
                    self.rpc_seqno = tv
                elif tn == "host_cpid":
                    self.host_cpid = tv
                elif tn == "total_credit":
                    self.total_credit = float(tv)
                elif tn == "expavg_credit":
                    self.expavg_credit = float(tv)
                elif tn == "domain_name":
                    self.domain_name = tv
                elif tn == "p_ncpus":
                    self.p_ncpus = int(tv)
                elif tn == "p_vendor":
                    self.p_vendor = tv
                elif tn == "p_fpops":
                    self.p_fpops = float(tv)
                elif tn == "p_iops":
                    self.p_iops = float(tv)
                elif tn == "os_name":
                    self.os_name = tv
                elif tn == "os_version":
                    self.os_version = tv

    def Show(self):
        print "----- host id: %s\n" \
              "  create time: %s\n" \
              "   rpc sequno: %s\n" \
              "    host cpid: %s\n" \
              " total credit: %f\n" \
              "expavg credit: %f\n" \
              "  domain name: %s\n" \
              "      p_ncpus: %d\n" \
              "     p_vendor: %s\n" \
              "      p_fpops: %f\n" \
              "       p_iops: %f\n" \
              "      os name: %s\n" \
              "   os version: %s\n" % (
                  self.id,
                  self.create_time,
                  self.rpc_seqno,
                  self.host_cpid,
                  self.total_credit,
                  self.expavg_credit,
                  self.domain_name,
                  self.p_ncpus,
                  self.p_vendor,
                  self.p_fpops,
                  self.p_iops,
                  self.os_name,
                  self.os_version)

def usage():
    print '''usage: check_credit.py [options]

options:
--proxy-server address  Specify the proxy server address.
--proxy-port port       Specify the proxy server port, 80 by default.
--show-hosts            Whether to show each host that belongs to account.
--help                  Print this help message.'''

def main():
    proxy_server = None
    proxy_port = 0
    show_hosts = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], '',
                ['help', 'proxy-server=', 'proxy-port=', 'show-hosts'])
    except optget.GetoptError, err:
        sys.stderr.write('%s\n' % err)
        usage()
        sys.exit(1)

    for opt_name, opt_value in opts:
        if opt_name == '--proxy-server':
            proxy_server = opt_value
            proxy_port = 80
        elif opt_name == '--proxy-port':
            try:
                proxy_port = int(opt_value)
            except ValueError:
                sys.stderr.write('port must be a numeric.\n')
                sys.exit(1)
        elif opt_name == '--show-hosts':
            show_hosts = True
        elif opt_name == '--help':
            usage()
            sys.exit()

    url = 'http://setiathome.berkeley.edu/show_user.php?' \
          'format=xml&auth=f0282faac4039735d53587a4ff4af014'
    if proxy_server:
        proxy_url = 'http://%s:%d' % (proxy_server, proxy_port)
        proxies = { 'http': proxy_url }
    else:
        proxies = None
    content = urllib.urlopen(url, proxies=proxies).read()
    xmldoc = parseString(content)

    user_info = UserInfo()
    user_info.Parse(xmldoc.documentElement)
    user_info.Show(show_hosts)

if __name__ == "__main__":
    main()
