#!/usr/bin/env python

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import sys
from struct import *


class PlotLine:

    def __init__(self, refresh=2):
        self.figure = plt.figure()
        self.refresh_per_second = refresh
        self.decimator = 8
        self.samples_per_second = 96*4*1000/4/self.decimator
        self.interval = 1000.0/self.refresh_per_second

        self.samples_per_plot = self.samples_per_second/refresh
        self.picker = 100

    def animate(self, i):
        ax = self.figure.add_subplot(1, 1, 1)

        data = ''
        data = sys.stdin.read(2*self.samples_per_plot)

        datay = []
        datay = unpack('<'+'h'*self.samples_per_plot, data)

        y_data = []
        x_data = []

        for i in range(self.samples_per_plot/self.picker):
            y_data.append(datay[i*self.picker])
            x_data.append(i*self.picker)


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
    plot = PlotLine()
    plot.run()
