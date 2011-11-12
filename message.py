from xml.dom import Node

class MESSAGE:
    def __init__(self):
        self.project   = ""
        self.priority  = 0
        self.seqno     = 0
        self.timestamp = 0
        self.body      = ""

    def parse(self, source):
        pass

    def show(self):
        pass
