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

    def generate_msg(self, number, sample = 0):
        return pack('<Qhhhhhhhh', number,sample,sample,sample,sample,sample,sample,sample,sample)

    def send(self, message):
        self.socket.connect('tcp://%s:%s' % (self.server_ip[-1], self.server_port[-1]))
        self.socket.send(message)

    def broadcast(self):
        for el in range(len(self.server_ip)):
            self.socket.connect("tcp://%s:%s" % (self.server_ip[el], self.server_port[el]))
            self.socket.send('Broadcasting message')
            print 'Sent to ' + 'tcp://%s:%s' % (self.server_ip[el], self.server_port[el])

    def single_shot(self):
        msg = self.generate_msg(1024)
        print len(msg)
        self.send(msg)

    def test(self, set):

        cntr = 0
        for session in range(250):
            msg = ''
            for i in range(192*4):
                cntr += 1
                msg += self.generate_msg(cntr, set*i)
            self.send(msg)


if __name__ == "__main__":
    address = sys.argv[1]
    port = sys.argv[2]
    print "Connect to %s:%s" % (address, port)

    client = ZMQClient()
    client.connect(address, port)

    if len(sys.argv) >= 4:
        client.test(int(sys.argv[4]))
    else:
        client.single_shot()
