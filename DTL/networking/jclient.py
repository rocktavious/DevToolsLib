import time
import json
import socket

from DTL.api import Logger
from DTL.networking.jsocket import JsonSocket

#------------------------------------------------------------
#------------------------------------------------------------
class JsonClient(JsonSocket):
    CONN_RETRY = 10

    #------------------------------------------------------------
    def __init__(self, address=None, port=None):
        super(JsonClient, self).__init__(address, port)
        self.timeout = 2

    #------------------------------------------------------------
    def connect(self):
        for i in range(JsonClient.CONN_RETRY):
            try:
                self.socket.connect( (self.address, self.port) )
            except socket.error as msg:
                self.logger.error("SockThread Error: %s" % msg)
                time.sleep(3)
                continue
            self.logger.info("...Socket Connected")
            return True
        return False

    #------------------------------------------------------------
    def run(self):
        while True:
            msg = raw_input('CLIENT >>> ')
            #Need to validate connect still exists
            self.send_obj({"message":msg})
            msg = client.read_obj()
            self.logger.info("client received: %s" % msg)            
         





if __name__ == '__main__':
    client = JsonClient()
    if client.connect():
        client.run()