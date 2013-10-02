# -*- coding: utf-8 -*-

from xml.dom import Node

class FILE_TRANSFER(object):
    def __init__(self):
        self.name                = ""
        self.project_url         = ""
        self.project_name        = ""
        self.nbytes              = 0.0
        self.generated_locally   = False
        self.uploaded            = False
        self.upload_when_present = False
        self.sticky              = False
        self.pers_xfer_active    = False
        self.xfer_active         = False
        self.num_retries         = 0
        self.first_request_time  = 0
        self.next_request_time   = 0
        self.status              = 0
        self.time_so_far         = 0.0
        self.bytes_xferred       = 0.0
        self.file_offset         = 0.0
        self.xfer_speed          = 0.0
        self.hostname            = ""
        self.project             = None # references an instance of class PROJECT

    def parse(self, source):
        pass

    def show(self):
        pass
