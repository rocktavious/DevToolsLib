import time
import json
import socket

from DTL.api import Logger
from DTL.networking.jsocket import JsonSocket

from DTL.api import Process

#------------------------------------------------------------
#------------------------------------------------------------
class JsonClient(JsonSocket, Process):
    CONN_RETRY = 10
    #------------------------------------------------------------
    def __init__(self, **kwds):
        Process.__init__(self)
        JsonSocket.__init__(self, *kwds)
        self.setTimeout(1000)

    #------------------------------------------------------------
    def main_loop(self):
        msg = raw_input('CLIENT >>> ')

        if msg == 'stop':
            self.stop()
            return
        
        self.send({"message":msg})
        msg = self.recv()
        self.logger.info("client received: %s" % msg)
        
    #------------------------------------------------------------
    def start(self):
        '''we override the start because we want the thread to handle calling run'''
        self.connect()
        super(JsonClient, self).start()
         





if __name__ == '__main__':
    client = JsonClient()
    client.start()