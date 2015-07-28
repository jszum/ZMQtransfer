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
        print 'Server is running on %s' % ("tcp://*:%s" % self.port)
        while True:
            message = self.socket.recv()
            print message
            self.socket.send("Accepted %s" % self.port)


if __name__ == "__main__":
    if len(sys.argv)==2:
        qport = int(sys.argv[1])
        server = ZMQserver(qport)

    else:
        server = ZMQserver()

    server.run()
