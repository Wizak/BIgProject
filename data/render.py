import numpy as np
import time
import matplotlib.pyplot as plt

from utils import read_data


plt.ion()


class DynamicUpdate():
    # Suppose we know the x range
    min_x = 0
    max_x = 1

    def on_launch(self):
        # Set up plot
        self.delay = 1
        self.figure, self.ax = plt.subplots()
        self.lines_bot, = self.ax.plot([], [])
        # Autoscale on unknown axis and known lims on the other
        self.ax.set_autoscaley_on(True)
        self.ax.set_xlim(self.min_x, self.max_x)
        # Other stuff
        self.ax.grid()
        ...

    def on_running(self, xdata, ydata):
        # Update data (with the new _and_ the old points)
        self.lines_bot.set_xdata(xdata[0])
        self.lines_bot.set_ydata(ydata[0])
        # Need both of these in order to rescale
        self.ax.relim()
        # We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    # Example
    def __call__(self, data):
        self.on_launch()
        xdata = [[]]
        ydata = [[]]
        data_value = [data[key] for key in data]
        print('Iter\tCPU\tGPU\tRAM')
        for x in range(len(data_value[-1])):
            xdata[0].append(x)
            ydata[0].append(data_value[0][x])
            # print(
            #     f'{x}\t{data_value[0][x]}\t{data_value[1][x]}\t{data_value[2][x]}')
            self.on_running(xdata, ydata)
            time.sleep(self.delay/60)
        return xdata, ydata


def main():
    delay = 0.1
    d = DynamicUpdate()
    bot_data = read_data('bot_usage.json')
    person_data = read_data('bot_usage.json')
    d(bot_data)


if __name__ == '__main__':
    main()
