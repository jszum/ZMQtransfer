#!/usr/bin/env python

import sys


class Writer:

    def __init__(self, fifo, csv):
        self.fifo = open()
        self.dest = open(csv,w+)


if __name__=='__main__':
    fifo = sys.argv[1]
    dest = sys.argv[2]