#!/usr/bin/python           # This is client.py file
'''
import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.

s.connect((host, port))
print s.recv(1024)
s.close                     # Close the socket when done
'''

import socket
import json

data = {'message':'hello world!', 'test':123.4}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 13373))
s.send(json.dumps(data))
result = json.loads(s.recv(1024))
print result
s.close()