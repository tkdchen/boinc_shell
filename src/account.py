# -*- coding: utf-8 -*-

import urllib
from md5 import md5
from xml.dom.minidom import Node
from xml.dom.minidom import parseString

class AccountInfo(object):
    pass


class _Account(object):

    @property
    def authenticator(self):
        return getattr(self, '_authenticator', None)

    @authenticator.setter
    def authenticator(self, value):
        self._authenticator = value

    @property
    def opaque_auth(self):
        return getattr(self, '_opaque_auth', None)

    @opaque_auth.setter
    def opaque_auth(self, value):
        self._opaque_auth = value

    @property
    def id(self):
        return getattr(self, 'id', None)

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return getattr(self, 'name', None)

    @name.setter
    def name(self, value):
        self._name = value

    def parse(self, xml):
        for node in xml.childNodes:
            if node.nodeType == Node.ELEMENT_NODE:
                setattr(self, node.nodeName, node.firstChild.nodeValue)

class Account(object):

    def get_credit(self):
        pass

    def update(self):
        pass

class AccountFactory(object):

    @staticmethod
    def lookup(project_url, email_addr, password):
        obj = md5()
        obj.update(password + email_addr)
        passwd_hash = obj.hexdigest()

        # First step: to get the authenticator and opaque_auth
        lookup_url = '%s/lookup_account.php?' \
                     'email_addr=%s&passwd_hash=%s&get_opaque_auth=1' % (
                             project_url.strip('/'), email_addr, passwd_hash)

        proxies = {'http':'http://10.11.101.3:8081'}
        s = urllib.urlopen(lookup_url, proxies=proxies).read()
        print s

        account = Account()

        nodes = parseString(s).documentElement.childNodes
        for node in nodes:
            if node.nodeType == Node.ELEMENT_NODE:
                setattr(account, node.nodeName, node.firstChild.nodeValue)

        return account

        # Second step: to get the account informations
        s = ''
        if hasattr(account, 'opaque_auth'):
             s = 'opaque_auth=%s' % account.opaque_auth
        s = '%s/am_get_info.php?account_key=%s&%s' % (project_url, account.authenticator, s)
        s = urllib.urlopen(s, proxies=proxies).read()

        # TODO: handling the xml response

        return account

if __name__ == '__main__':
    account = AccountFactory.lookup('http://einstein.phys.uwm.edu/', 'qcxhome@gmail.com', 'qcxeinsteinhome')
    print account.authenticator

    account = AccountFactory.lookup('http://boinc.bakerlab.org/rosetta/', 'qcxhome@gmail.com', 'qcxrosettahome')
    print account.authenticator
