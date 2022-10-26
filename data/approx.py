import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from utils import read_data


def drawing(x, y):
    plt.figure(figsize=(8, 6))
    plt.title("Human - RAM usage")
    plt.xlabel("Seconds")
    plt.ylabel("Usages")

    plt.scatter(x, y)

    legend = []
    # аргументы для построения графиков моделей: исходный интервал + 60 дней
    fx = sp.linspace(x[0], x[-1] + 60, 1000)
    for d in range(1, 4):
        fp, residuals, rank, sv, rcond = sp.polyfit(x, y, d, full=True)
        f = sp.poly1d(fp)
        plt.plot(fx, f(fx), linewidth=2)
        legend.append("d=%i" % f.order)
        f2 = f - 1000
        t = fsolve(f2, x[-1])
    plt.legend(legend, loc="upper left")
    plt.grid()

    plt.show()


def main():
    data = read_data('human_usage.json')
    data_value = [data[key] for key in data]

    x = [x for x in range(len(data_value[-1]))]
    y = [y for y in data_value[2]]
    drawing(x, y)


if __name__ == '__main__':
    main()
