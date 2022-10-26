import time
import numpy as np

from utils import psutility, save_data


DATA = {'CPU': [], 'GPU': [], 'RAM': []}


def write_data(state):
    global DATA

    for key, value in zip(DATA.keys(), state):
        DATA[key].append(round(value, 1))


def main(start=0, end=10, delay=1):
    step = delay/60
    for x in np.arange(start, end, step):
        state = psutility()
        write_data(state)
        save_data(DATA)
        time.sleep(delay)


if __name__ == '__main__':
    main(0, 5, 1)
