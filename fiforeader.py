#!/usr/bin/env python

from struct import *
import os
fifo = 'zmqfifo'

class Reader:

    def __init__(self, port=54001):
        self.readings = 192*4
        self.fifo = fifo

    def run(self):
        bin = os.open(self.fifo, os.O_RDWR)

        while True:
            record = ''
            msg = os.read(bin, 24*self.readings)
            for i in range(self.readings):
                    buffer = msg[24*i:24*(i+1)]
                    if len(buffer)==24:
                        unpck = unpack('<Qhhhhhhhh', buffer)
                        record += ';'.join(str(e) for e in unpck)+';\n'
            self.saveCSV(record)

    def saveCSV(self, record):
        csv = open('data.csv', 'wa+')
        csv.write(record)
        csv.close()

def clean():
    try:
        os.unlink(fifo)
    except:
        pass
    os.mkfifo(fifo)

if __name__ == "__main__":

    clean()
    reader = Reader()
    reader.run()
