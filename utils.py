from io import BytesIO
from PIL import Image

import cv2
import numpy as np
import os
import base64
import json
import win32gui
import sys


def get_file_path(filename):
    bundle_dir = getattr(
        sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    path_to_file = os.path.abspath(os.path.join(bundle_dir, filename))
    return path_to_file


def init_config(conf_file=None, file_path='config.json'):
    file_path = get_file_path(file_path)

    if conf_file is None:
        mode = 'r'
    else:
        mode = 'w'

    with open(file_path, mode) as file:
        if mode == 'r':
            conf_file = json.load(file)
            return conf_file
        json.dump(conf_file, file, indent=4)


def get_titles():
    WINDOW_LIST = []

    def winEnumHandler(hwnd, ctx):
        nonlocal WINDOW_LIST
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)
            if window_title != '':
                WINDOW_LIST.append(window_title)

    win32gui.EnumWindows(winEnumHandler, None)
    return WINDOW_LIST


def resize_image(filename, image_size):
    abs_path = get_file_path(filename)
    img = Image.open(abs_path)
    resized_img = img.resize(image_size)
    buffered = BytesIO()
    resized_img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str


def label_detecting(stream):
    return stream


def output_stream(stream, image_size, detecting=False):
    if detecting:
        stream = label_detecting(stream)
    img = Image.fromarray(np.uint8(stream))
    resized_img = img.resize(image_size)
    imgbytes = cv2.imencode('.png', np.asarray(resized_img))[1]
    return imgbytes.tobytes()
