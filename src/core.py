# -*- coding: utf-8 -*-

from socket import *
from xml.dom.minidom import parseString
from xml.dom import Node
from project import PROJECTS
from result import RESULTS
from version import *
from definition import GUI_RPC_AUTH_CONFIG

LOCAL_HOST        = "localhost"
LOCAL_LOOPBACK_IP = "127.0.0.1"
GUI_RPC_PORT      = 1043

RPC_REQUEST_TEMPLATE = "<boinc_gui_rpc_request>\n" \
                       "   <major_version>%d</major_version>\n" \
                       "   <minor_version>%d</minor_version>\n" \
                       "   <release>%d</release>\n" \
                       "%s\n" \
                       "</boinc_gui_rpc_request>\n\003"

class shell_core(object):
    """
    shell core code
    """
    def __init__(self):
        self.sock = None
        self._boinc_pwd = ""

        # read boinc pwd from config file
        fh = open(GUI_RPC_AUTH_CONFIG, "r+")
        self._boinc_pwd = fh.readline()
        fh.close()

    def prepare(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((gethostbyname(LOCAL_HOST), GUI_RPC_PORT))

    def done(self):
        self.sock.shutdown(SHUT_RDWR)
        self.sock.close()

    def send_request(self, request):
        s = RPC_REQUEST_TEMPLATE % (
            BOINC_MAJOR_VERSION,
            BOINC_MINOR_VERSION,
            BOINC_RELEASE,
            request)

        self.sock.send(s)

    def rpc_reply(self):
        buffer_size = 1024
        result = ""
        dorecv = True
        while dorecv:
            resbuf = self.sock.recv(buffer_size)
            if ord(resbuf[-1:]) == 3:
                result += resbuf[0:-1]
                dorecv = False
            else:
                result += resbuf
        return result

    def md5_block(self, source):
        import md5
        buf = md5.new(source).digest()
        result = ""
        r = range(len(buf))
        for i in r:
            hv = "%02x" % (ord(buf[i]))
            result += hv
        return result

    def get_nonce(self, source):
        """
        Get nonce value
        """
        try:
            xmldoc = parseString(source)
        except:
            return None
        nodes = xmldoc.getElementsByTagName("nonce")
        if len(nodes) > 0:
            return nodes[0].firstChild.nodeValue
        return None

    def authorize(self):
        from rpc_call import AUTH1, AUTH2

        self.sock.send(AUTH1)
        nonce = self.get_nonce(self.rpc_reply())
        if nonce == None: return False
        self.sock.send(AUTH2 % (self.md5_block(nonce + self._boinc_pwd)))
        try:
            xmldoc = parseString(self.rpc_reply())
        except:
            return False
        return len(xmldoc.getElementsByTagName("authorized")) > 0

    def get_results(self):
        """
        Sending <get_results/> to BOINC server to get current results
        """
        from rpc_call import GET_RESULTS

        self.send_request(GET_RESULTS)
        xmldoc = parseString(self.rpc_reply())

        results = RESULTS()
        results.parse(xmldoc.documentElement)

        return results

    def get_projects(self):
        """
        sending <get_project_status/> to BOINC server to get current projects' status
        """
        from rpc_call import GET_PROJECT_STATUS

        self.send_request(GET_PROJECT_STATUS)
        xmldoc = parseString(self.rpc_reply())

        projects = PROJECTS()
        projects.parse(xmldoc.documentElement)

        return projects

    def quit_boinc(self):
        """
        Send <quit/> to quit from BOINC
        """
        from rpc_call import QUIT

        self.send_request(QUIT)

    def set_project(self, project, value):
        """
        valid value: reset, detach, update, nomorework, allowmorework
        """
        from rpc_call import PROJECT_RESET, PROJECT_DETACH, PROJECT_UPDATE
        from rpc_call import PROJECT_NOMOREWORK, PROJECT_ALLOWMOREWORK
        from rpc_call import PROJECT

        rc = {
                'reset': PROJECT_RESET,
                'detach': PROJECT_DETACH,
                'update': PROJECT_UPDATE,
                'nomorework': PROJECT_NOMOREWORK,
                'allowmorework': PROJECT_ALLOWMOREWORK
             }[value]
        self.send_request(rpc_call.PROJECT % (rc, project.master_url, rc))

    def set_result(self, project, result, operation):
        from rpc_call import SUSPEND_RESULT, ABORT_RESULT, RESUME_RESULT
        from rpc_call import RESULT

        op = {
                'suspend': SUSPEND_RESULT,
                'abort': ABORT_RESULT,
                'resume': RESUME_RESULT
             }[operation]
        self.send_request(RESULT % (op, project.master_url, result.name, op))

    def get_file_transfers(self):
        from rpc_call import GET_FILE_TRANSFERS

        self.send_request(GET_FILE_TRANSFERS);
        print self.rpc_reply()

