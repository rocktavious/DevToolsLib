"""
Contains JsonSocket, JsonServer and JsonClient implementations (json object message passing server and client).

This file is part of the jsocket package.
Copyright (C) 2011 by 
Christopher Piekarski <chris@cpiekarski.com>

The jsocket_base module is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

The jsocket package is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with jsocket_base module.  If not, see <http://www.gnu.org/licenses/>.


Modified by Kyle Rockman

"""
import json
import socket
import struct
import time

from DTL.api import Logger

DEFAULT_PORT = 5489
ADDRESS_FAMILY = socket.AF_INET
SOCKET_TYPE = socket.SOCK_STREAM

#------------------------------------------------------------
def getLocalIP():
    '''A helper function that will try to get the local IP address in a multiplatform way'''
    addr = socket.gethostbyname(socket.gethostname())
    if addr == "127.0.0.1" : #Try internet connection method
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('google.com',0))
        addr = s.getsockname()[0]
    return addr

#------------------------------------------------------------
#------------------------------------------------------------
class JsonSocket(object):
    __metaclass__ = Logger.getMetaClass()
    #------------------------------------------------------------
    def __init__(self, address=None, port=None):
        self.socket = socket.socket(ADDRESS_FAMILY, SOCKET_TYPE)
        self.conn = self.socket
        self._timeout = None
        self._address = address or getLocalIP()
        self._port = port or DEFAULT_PORT
    
    #------------------------------------------------------------
    def send_obj(self, obj):
        msg = json.dumps(obj)
        if self.socket:
            frmt = "=%ds" % len(msg)
            packed_msg = struct.pack(frmt, msg)
            packed_hdr = struct.pack('!I', len(packed_msg))

            self._send(packed_hdr)
            self._send(packed_msg)
        
    #------------------------------------------------------------
    def _send(self, msg):
        sent = 0
        while sent < len(msg):
            sent += self.conn.send(msg[sent:])
    
    #------------------------------------------------------------
    def _read(self, size):
        data = ''
        while len(data) < size:
            data_tmp = self.conn.recv(size-len(data))
            data += data_tmp
            if data_tmp == '':
                raise RuntimeError("socket connection broken")
        return data
    
    #------------------------------------------------------------
    def _msg_length(self):
        d = self._read(4)
        s = struct.unpack('!I', d)
        return s[0]
    
    #------------------------------------------------------------
    def read_obj(self):
        size = self._msg_length()
        data = self._read(size)
        frmt = "=%ds" % size
        msg = struct.unpack(frmt, data)
        return json.loads(msg[0])
    
    #------------------------------------------------------------
    def close(self):
        self._close_socket()
        if self.socket is not self.conn:
            self._close_connection()
    
    #------------------------------------------------------------
    def _close_socket(self):
        self.logger.debug("closing main socket")
        self.socket.close()
    
    #------------------------------------------------------------
    def _close_connection(self):
        self.logger.debug("closing the connection socket")
        self.conn.close()
    
    #------------------------------------------------------------
    def _get_timeout(self):
        return self._timeout
    
    #------------------------------------------------------------
    def _set_timeout(self, timeout):
        self._timeout = timeout
        self.socket.settimeout(timeout)
    
    #------------------------------------------------------------
    def _get_address(self):
        return self._address
    
    #------------------------------------------------------------
    def _set_address(self, address):
        pass
    
    #------------------------------------------------------------
    def _get_port(self):
        return self._port
    
    #------------------------------------------------------------
    def _set_port(self, port):
        pass

    #------------------------------------------------------------
    timeout = property(_get_timeout, _set_timeout,doc='Get/set the socket timeout')
    address = property(_get_address, _set_address,doc='read only property socket address')
    port = property(_get_port, _set_port,doc='read only property socket port')




if __name__ == "__main__":
    """ basic json echo server """
    
    logger = Logger.getSubLogger('JSONECHOTEST')

    def server_thread():
        logger.debug("starting JsonServer")
        server = JsonServer()
        server.accept_connection()
        while 1:
            try:
                msg = server.read_obj()
                logger.info("server received: %s" % msg)
                server.send_obj(msg)
            except socket.timeout as e:
                logger.debug("server socket.timeout: %s" % e)
                continue
            except Exception as e:
                logger.error("server: %s" % e)
                break

        server.close()

    t = threading.Timer(1,server_thread)
    t.start()

    time.sleep(2)
    logger.debug("starting JsonClient")

    client = JsonClient()
    client.connect()

    i = 0
    while i < 10:
        client.send_obj({"i": i})
        try:
            msg = client.read_obj()
            logger.info("client received: %s" % msg)
        except socket.timeout as e:
            logger.debug("client socket.timeout: %s" % e)
            continue
        except Exception as e:
            logger.error("client: %s" % e)
            break
        i = i + 1

    client.close()