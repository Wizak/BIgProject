import matplotlib.pyplot as plt
from utils import read_data
import numpy as np


def moving_avg(x, n):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[n:] - cumsum[:-n]) / float(n)


def main():
    data = read_data('bot_usage.json')
    data_value = [data[key] for key in data]
    data_x = [x for x in range(len(data_value[-1]))]
    data_y = [y for y in data_value[2]]

    avg_y = moving_avg(data_y, 15)
    avg_x = [i for i in range(len(avg_y))]
    draw(data_x, data_y, avg_x, avg_y)
    avg_usage = round(sum(data_y)/len(data_y), 1)
    print(f'BOT RAM: {avg_usage}%')


def draw(data_x, data_y, avg_x, avg_y):
    plt.figure()
    plt.plot(data_x, data_y, linewidth=1, label='normal')
    plt.plot(avg_x, avg_y, linewidth=4, label='average')
    plt.xlabel('Seconds')
    plt.ylabel('Usages')
    plt.title('Bot - CPU usage')
    plt.legend()
    plt.grid()
    plt.show()


if __name__ == '__main__':
    main()
