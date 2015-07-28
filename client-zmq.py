#!/usr/bin/env python

import zmq
import sys

class ZMQClient:

    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.address = ''
        self.port = ''

    def connect(self, adr, port):
        self.address = adr
        self.port = port

    def send(self):
        self.socket.connect('tcp://%s:%s' % (self.address, self.port))
        self.socket.send('Test message')
        print 'sended to ' + 'tcp://%s:%s' % (self.address, self.port)

if __name__ == "__main__":
    qaddress = sys.argv[1]
    qport = sys.argv[2]
    print "Connect to %s:%s" % (qaddress, qport)

    client = ZMQClient()
    client.connect(qaddress, qport)
    client.send()
