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
        self.readings = 192*4

        self.binary = datetime.datetime.now().isoformat()[:-6]+'bin'
        bin = open(self.binary, 'wb+')
        bin.close()

    def run(self):
        print 'Server is running on %s' % ("tcp://*:%s" % self.port)
        while True:
            message = ''
            message = self.socket.recv()
            self.saveBin(message)

            #record = ''
            # for i in range(self.readings):
            #     buffer = message[24*i:24*(i+1)]
            #     unpck = unpack('<Qhhhhhhhh', buffer)
            #     self.binary.write(str(unpck))
            #     #record += ';'.join(str(e) for e in unpck)+';\n'

            #self.saveTo(record)

    def saveBin(self, message):
        bin = open(self.binary, 'awb+')
        bin.write(message)
        bin.close()

if __name__ == "__main__":
    if len(sys.argv)==2:
        qport = int(sys.argv[1])
        server = ZMQserver(qport)

    else:
        server = ZMQserver()

    server.run()
