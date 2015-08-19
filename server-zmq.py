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

    def run(self):
        sys.stderr.write('Server is running on %s' % ("tcp://*:%s" % self.port))
        while True:
            message = ''
            message = self.socket.recv()
            self.saveBin(message)
            sys.stdout.write(message)

    def saveBin(self, message):
        binar = open(self.binary, 'awb+')
        binar.write(message)
        binar.close()

if __name__ == "__main__":

    if len(sys.argv) == 2:
        port = int(sys.argv[1])
        server = ZMQserver(port)

    else:
        server = ZMQserver()

    server.run()
