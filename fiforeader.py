#!/usr/bin/env python

from struct import *
import os
import sys
import array

fifo = 'zmqfifo'


class Reader:

    def __init__(self, csv="aa.csv"):
        self.readings = 192*4
        self.csv = csv
        self.channel = 2
        self.fifo = os.open('zmqfifo', os.O_RDWR | os.O_NONBLOCK)


    def run(self):
        while True:
            record = ''
            rawdata = []

            rawdata.append(array.array('h'))

            msg = ''
            msg = sys.stdin.read(24*self.readings)
            sys.stdin.flush()

            for i in range(self.readings):
                buffer = msg[24*i:24*(i+1)]

                if len(buffer) == 24:
                    unpck = unpack('<Qhhhhhhhh', buffer)

                    rawdata[0].append(unpck[self.channel+1])

            try:
                print 'Write'
                os.write(self.fifo, rawdata[0])
            except OSError, e:
                pass
            #sys.stdout.write(rawdata[0].tostring())
            #record += ';'.join(str(e) for e in unpck)+';\n'

    def saveCSV(self, record):
        csv = open(self.csv + '.csv', 'wa+')
        csv.write(record)
        csv.close()


def clean():
    try:
        os.unlink('zmqfifo')
    except:
        pass

    os.mkfifo('zmqfifo')

if __name__ == "__main__":

    clean()
    reader = Reader()
    reader.run()

