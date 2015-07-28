#!/usr/bin/env python

import zmq
import sys

class ZMQserver:

    def __init__(self, port=5556):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:%s" % port)
        self.port = port

    def run(self):
        print 'Server is running'
        while True:
            message = self.socket.recv()
            print message



if __name__ == "__main__":
    qport = int(sys.argv[1])
    print qport

    server = ZMQserver()
    server.run()