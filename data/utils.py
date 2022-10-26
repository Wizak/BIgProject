import psutil
import GPUtil
import json


def psutility():
    cpu = psutil.cpu_percent(0)
    gpu = GPUtil.getGPUs()[-1].load*100
    ram = psutil.virtual_memory().percent

    return cpu, gpu, ram


def read_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def save_data(state):
    with open('monitor_usage.json', 'w') as f:
        json.dump(state, f, indent=4)
