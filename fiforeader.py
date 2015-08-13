#!/usr/bin/env python

from struct import *
import os
import sys
import array

fifo = 'zmqfifo'

class Reader:

    def __init__(self, csv="d.csv"):
        self.readings = 192*4
        self.csv = csv
        self.channel = 2

    def run(self):
        while True:
            record = ''
            rawdata = []

            rawdata.append(array.array('h'))

            msg = sys.stdin.read(24*self.readings)

            for i in range(self.readings):
                buffer = msg[24*i:24*(i+1)]

                if len(buffer) == 24:
                    unpck = unpack('<Qhhhhhhhh', buffer)

                    rawdata[0].append(unpck[self.channel+1])

            sys.stdout.write(rawdata[0].tostring())
            #record += ';'.join(str(e) for e in unpck)+';\n'
            #self.saveCSV(record)

    def saveCSV(self, record):
        csv = open(self.csv + '.csv', 'wa+')
        csv.write(record)
        csv.close()

if __name__ == "__main__":

    #csvfile = sys.argv[1]
    reader = Reader()
    reader.run()
