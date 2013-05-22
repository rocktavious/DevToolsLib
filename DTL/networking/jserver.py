import time
import threading
import socket
import json

from DTL.networking.jsocket import JsonSocket

class JsonServer(JsonSocket):
    def __init__(self, address=None, port=None):
        super(JsonServer, self).__init__(address, port)
        self._bind()

    def _bind(self):
        self.socket.bind( (self.address,self.port) )
        self.logger.info('Server running on {0}:{1}'.format(self.address, self.port))

    def _listen(self):
        self.socket.listen(1)

    def _accept(self):
        return self.socket.accept()

    def accept_connection(self):
        self._listen()
        self.conn, addr = self._accept()
        self.conn.settimeout(self.timeout)
        self.logger.info("connection accepted from ({0}:{1})".format(addr[0] ,addr[1]))

    def _is_connected(self):
        return True if not self.conn else False

    connected = property(_is_connected, doc="True if server is connected")

class JsonThreadedServer(threading.Thread, JsonServer):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        JsonServer.__init__(self, **kwargs)
        self._isAlive = False

    def _process_message(self, obj):
        """ Pure Virtual Method

        	This method is called every time a JSON object is received from a client

        	@param	obj	JSON "key: value" object received from client
        	@retval	None
        """
        pass

    def run(self):
        while self._isAlive:
            try:
                self.accept_connection()
            except socket.timeout as e:
                self.logger.info("socket.timeout: %s" % e)
                continue
            except Exception as e:
                self.logger.exception(e)
                continue

            while self._isAlive:
                try:
                    obj = self.read_obj()
                    self._process_message(obj)
                except socket.timeout as e:
                    self.logger.info("socket.timeout: %s" % e)
                    continue
                except Exception as e:
                    self.logger.exception(e)
                    self._close_connection()
                    break
            self.close()
            
    def handle_input(self):
        #myLock.acquire()
        msg = raw_input('Prompt>>>')
        if msg == 'stop' :
            self.stop()
            self.close()
            return
        print "Received {0}".format(msg)
        #myLock.release()
        self.loop()
            
    def loop(self):
        try:
            while True:
                time.sleep(100)
        except KeyboardInterrupt:
            self.handle_input()

    def start(self):
        """ Starts the threaded server. 
        	The newly living know nothing of the dead

        	@retval None	
        """
        self._isAlive = True
        super(JsonThreadedServer, self).start()
        self.logger.info("Threaded Server has been started.")
        self.loop()

    def stop(self):
        """ Stops the threaded server.
        	The life of the dead is in the memory of the living 

        	@retval None	
        """
        self._isAlive = False
        self.logger.info("Threaded Server has been stopped.")

class ServerFactoryThread(threading.Thread, JsonSocket):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self, **kwargs)
        JsonSocket.__init__(self, **kwargs)

    def swap_socket(self, new_sock):
        """ Swaps the existing socket with a new one. Useful for setting socket after a new connection.

        	@param	new_sock	socket to replace the existing default jsocket.JsonSocket object	
        	@retval	None
        """
        del self.socket
        self.socket = new_sock
        self.conn = self.socket

    def run(self):
        while self.isAlive():
            try:
                obj = self.read_obj()
                self._process_message(obj)
            except socket.timeout as e:
                self.logger.info("socket.timeout: %s" % e)
                continue
            except Exception as e:
                self.logger.info("client connection broken, closing socket")
                self._close_connection()
                break
        self.close()

class ServerFactory(JsonThreadedServer):
    def __init__(self, server_thread, **kwargs):
        JsonThreadedServer.__init__(self, **kwargs)
        if not issubclass(server_thread, ServerFactoryThread):
            raise TypeError("serverThread not of type", ServerFactoryThread)
        self._thread_type = server_thread
        self._threads = []

    def run(self):
        while self._isAlive:
            tmp = self._thread_type()
            self._purge_threads()
            while not self.connected and self._isAlive:
                try:
                    self.accept_connection()
                except socket.timeout as e:
                    self.logger.info("socket.timeout: %s" % e)
                    continue
                except Exception as e:
                    self.logger.exception(e)
                    continue
                else:
                    tmp.swap_socket(self.conn)
                    tmp.start()
                    self._threads.append(tmp)
                    break

        self._wait_to_exit()		
        self.close()

    def stop_all(self):
        for t in self._threads:
            if t.isAlive():
                t.exit()
                t.join()

    def _purge_threads(self):
        for t in self._threads:
            if not t.isAlive():
                self._threads.remove(t)

    def _wait_to_exit(self):
        while self._get_num_of_active_threads():
            time.sleep(0.2)

    def _get_num_of_active_threads(self):
        return len([True for x in self._threads if x.isAlive()])

    active = property(_get_num_of_active_threads, doc="number of active threads")


if __name__ == '__main__':
    class MyFactoryThread(ServerFactoryThread):
        """	This is an example factory thread, which the server factory will
        instantiate for each new connection.
        """
        def __init__(self):
            super(MyFactoryThread, self).__init__()
            self.timeout = 2.0
    
        def _process_message(self, obj):
            """ virtual method - Implementer must define protocol """
            if obj != '':
                if obj['message'] == "new connection":
                    self.send_obj({'action':'new connections'})
                
                self.logger.info("{0} :: {1}".format(self.conn_addr, obj))
    
    server = ServerFactory(MyFactoryThread)
    server.start()