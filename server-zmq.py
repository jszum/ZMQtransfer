#!/usr/bin/env python

import zmq
import sys
import os
import struct

fifo = 'zmqfifo'


class ZMQserver:

    def __init__(self, port=5556):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:%s" % port)
        self.port = port
        self.readings = 192

        self.fifo = open(fifo, 'w')

    def run(self):
        print 'Server is running on %s' % ("tcp://*:%s" % self.port)
        while True:

            message = self.socket.recv()
            self.fifo.write(message)

def clean(name):
    try:
        os.unlink(name)
    except:
        pass


if __name__ == "__main__":
    if len(sys.argv)==2:
        qport = int(sys.argv[1])
        server = ZMQserver(qport)

    else:
        server = ZMQserver()

    clean(fifo)
    os.mkfifo(fifo)
    server.run()
