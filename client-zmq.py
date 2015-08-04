#!/usr/bin/env python

import zmq
import sys
from struct import *

class ZMQClient:

    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUSH)
        self.server_ip = []
        self.server_port = []

    def connect(self, adr, port):
        self.server_ip.append(adr)
        self.server_port.append(port)

    def send(self):
        self.socket.connect('tcp://%s:%s' % (self.server_ip[-1], self.server_port[-1]))
        message = pack('>Qhhhhhhhh', 65554,512,0,0,0,0,0,0,0)#,65555,513,0,0,0,0,0,0,0)
        self.socket.send(message)
        print 'Sent to ' + 'tcp://%s:%s' % (self.server_ip[-1], self.server_port[-1])

    def broadcast(self):
        for el in range(len(self.server_ip)):
            self.socket.connect("tcp://%s:%s" % (self.server_ip[el], self.server_port[el]))
            self.socket.send('Broadcasting message')
            print 'Sent to ' + 'tcp://%s:%s' % (self.server_ip[el], self.server_port[el])



if __name__ == "__main__":
    address = sys.argv[1]
    port = sys.argv[2]
    print "Connect to %s:%s" % (address, port)

    client = ZMQClient()
    client.connect(address, port)
    client.send()
