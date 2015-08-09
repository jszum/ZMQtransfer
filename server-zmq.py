#!/usr/bin/env python

import zmq
import sys
from struct import *
import datetime

fifo = 'zmqfifo'

class ZMQserver:

    def __init__(self, port=54001):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        self.socket.bind("tcp://*:%s" % port)
        self.port = port

        self.binary = datetime.datetime.now().isoformat()[:-6]+'bin'
        binar = open(self.binary, 'wb+')
        binar.close()

        self.fifo = fifo

    def run(self):
        print 'Server is running on %s' % ("tcp://*:%s" % self.port)
        while True:
            message = ''
            message = self.socket.recv()
            print "."
            self.saveBin(message)
            self.saveFIFO(message)

    def saveBin(self, message):
        binar = open(self.binary, 'awb+')
        binar.write(message)
        binar.close()
        
    def saveFIFO(self, message):
            fif = open(self.fifo, 'wb')
            fif.write(message)
            fif.close()

if __name__ == "__main__":

    if len(sys.argv) == 2:
        port = int(sys.argv[1])
        server = ZMQserver(port)

    else:
        server = ZMQserver()

    server.run()
