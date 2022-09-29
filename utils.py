from io import BytesIO
from PIL import Image

import cv2
import os
import base64
import json
import win32gui
import sys


DEFAULT_CONFIG = {
    "FPS": 20,
    "WINDOW_SIZE": [
        640,
        360
    ],
    "DISCONNECT_INFO": "disconnect_info.png",
    "WINDOW_ICON": "window_icon.ico"
}


def get_file_path(filename):
    bundle_dir = getattr(
        sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    path_to_file = os.path.abspath(
        os.path.join(bundle_dir, 'static/' + filename))
    return path_to_file


def init_config(conf_file=None, file_path='config.json'):
    file_path = get_file_path(file_path)

    if conf_file is None:
        mode = 'r'
    else:
        mode = 'w'

    file_creating = True
    while True:
        if os.path.exists(file_path):
            with open(file_path, mode) as file:
                if mode == 'r':
                    conf_file = json.load(file)
                    return conf_file
                json.dump(conf_file, file, indent=4)
            break
        if file_creating:
            with open(file_path, 'w') as file:
                json.dump(DEFAULT_CONFIG, file, indent=4)
            file_creating = False


def get_perm(filename, directory, window, values):
    if filename != '' and directory != '':
        if filename in os.listdir(directory):
            abs_path = os.path.join(directory, filename)
            with open(abs_path, 'r') as file:
                ready_check = json.load(file)
            if ready_check['READY'] and values['-TARGET WINDOW-'] == ready_check['WINDOW']:
                window['-START-'].update(disabled=False)
                return True
    window['-START-'].update(disabled=True)
    return False


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


def create_image(image_size):
    img = Image.new('RGB', image_size, color='black')
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str


def resize_image(filename, image_size):
    abs_path = get_file_path(filename)
    img = Image.open(abs_path)
    resized_img = img.resize(image_size)
    buffered = BytesIO()
    resized_img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str


def label_detecting(stream, detector):
    detections = detector.detectObjectsFromImage(
        input_image=stream,
        input_type='array',
        output_type='array',
        minimum_percentage_probability=40,
        extract_detected_objects=True,
        thread_safe=False
    )
    return detections[0], detections[1]


def output_stream(stream, image_size, detector, detecting=True):
    detections = None
    if detecting:
        stream, detections = label_detecting(stream, detector)
    resized = cv2.resize(
        stream, image_size, interpolation=cv2.INTER_AREA)
    imgbytes = cv2.imencode('.png', resized)[1].tobytes()
    return detections, imgbytes
