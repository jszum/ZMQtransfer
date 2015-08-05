#!/usr/bin/env python

import zmq
import sys
from struct import *

fifo = 'zmqfifo'

class ZMQserver:

    def __init__(self, port=54001):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        self.socket.bind("tcp://*:%s" % port)
        self.port = port
        self.readings = 192*4
        self.csv = 'data.csv'
        self.fifo = fifo
        self.file = open(self.csv, 'w+')


    def run(self):
        print 'Server is running on %s' % ("tcp://*:%s" % self.port)
        while True:
            message = ''
            message = self.socket.recv()
            record = ''

            for i in range(self.readings):
                buffer = message[24*i:24*(i+1)]
                unpck = unpack('<Qhhhhhhhh', buffer)
                record += ';'.join(str(e) for e in unpck)+';\n'

            self.saveTo(record)

    def saveTo(self, message):
        self.file.write(message)

if __name__ == "__main__":
    if len(sys.argv)==2:
        qport = int(sys.argv[1])
        server = ZMQserver(qport)

    else:
        server = ZMQserver()

    server.run()
