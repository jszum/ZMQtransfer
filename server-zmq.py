#!/usr/bin/env python

import zmq
import sys
from struct import *
import datetime
import posix_ipc as ipc
import mmap

fifo = 'zmqfifo'

record = ipc.SharedMemory('/rec', ipc.O_CREAT, size=2)
r = mmap.mmap(record.fd, 2)
r.write('0')

name = ipc.SharedMemory('/file', ipc.O_CREAT, size=19)
n = mmap.mmap(name.fd, 19)


class ZMQserver:

    def __init__(self, port=54001):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        self.socket.bind("tcp://*:%s" % port)
        self.port = port

        self.rec = 0


    def run(self):
        sys.stderr.write('Server is running on %s' % ("tcp://*:%s" % self.port))
        while True:
            message = ''
            message = self.socket.recv()
            self.saveBin(message)
            sys.stdout.write(message)

    def saveBin(self, message):
        r.seek(0)
        self.rec = int(r.read(1))

        if self.rec == 1:
            n.seek(0)
            filename = str(n.read(19))
            binar = open(filename.rstrip('\0')+'.bin', 'awb+')
            binar.write(message)
            binar.close()

if __name__ == "__main__":

    if len(sys.argv) == 2:
        port = int(sys.argv[1])
        server = ZMQserver(port)

    else:
        server = ZMQserver()

    server.run()
