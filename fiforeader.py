#!/usr/bin/env python

from struct import *
import os
import array

fifo = 'zmqfifo'

class Reader:

    def __init__(self, csv):
        self.readings = 192*4
        self.fifo = fifo
        self.csv = csv

    def run(self):
        bin = os.open(self.fifo, os.O_RDONLY)

        while True:
            record = ''
            rawdata = []

            for i in range(8):
                rawdata.append(array.array('h'))

            msg = os.read(bin, 24*self.readings)

            for i in range(self.readings):
                buffer = msg[24*i:24*(i+1)]

                if len(buffer) == 24:
                    unpck = unpack('<Qhhhhhhhh', buffer)
                    for f in range(8):
                        rawdata[f].append(unpck[f+1])

                    record += ';'.join(str(e) for e in unpck)+';\n'

            self.saveCSV(record)
            self.split(rawdata)

    def saveCSV(self, record):
        csv = open(self.csv + '.csv', 'wa+')
        csv.write(record)
        csv.close()

    def split(self, rec):
        for f in range(8):
            data = pack('h'*self.readings, *rec[f])
            file = open('fifo'+str(f), 'wab+')
            file.write(data)
            file.close()


def clean():
    try:
        for i in range(8):
            os.unlink('fifo'+str(i))
    except:
        pass
    for i in range(8):
        os.mkfifo('fifo'+str(i))

if __name__ == "__main__":

    clean()
    csvfile = sys.argv[1]
    reader = Reader(csvfile)
    reader.run()
