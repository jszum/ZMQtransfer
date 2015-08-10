#!/usr/bin/env python

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import sys
from struct import *


class PlotLine:

    def __init__(self, channel, interval=100):
        self.figure = plt.figure()
        self.interval = interval
        self.sample_rate = 48000
        self.samples_per_plot = 192*4

        file = 'fifo'+str(channel)
        self.fifo = os.open(file, os.O_RDWR)

    def animate(self, i):
        ax = self.figure.add_subplot(1, 1, 1)

        data = ''
        data = os.read(self.fifo, 2*self.samples_per_plot)
        y_data = []
        y_data = unpack('h'*self.samples_per_plot, data)

        x_data = []
        length = len(y_data)
        for i in range(length):
            x_data.append(i)

        ax.clear()
        ax = plt.gca()
        ax.set_xlim(0, self.samples_per_plot)

        limit = 32768

        ax.set_ylim(-limit, limit)
        ax.plot(x_data, y_data)

    def run(self):
        ani = animation.FuncAnimation(self.figure, self.animate, interval=self.interval)
        plt.show()

if __name__ == '__main__':
    print(' '.join(sys.argv))
    channel = 1#sys.argv[1]

    plot = PlotLine(channel)
    plot.run()
