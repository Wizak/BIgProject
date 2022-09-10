from windowcapture import WindowCapture
from components import layout_all
from utils import (
    resize_image,
    init_config,
    output_stream,
    get_titles
)

import PySimpleGUI as sg


def start_event(values):
    global STREAMING, DETECTING
    STREAMING = True
    if values['-TARGET FOLDER-'] and values['-TARGET WINDOW-']:
        DETECTING = True


def pause_event():
    global STREAMING, DETECTING
    STREAMING = not STREAMING
    DETECTING = not DETECTING


def targetWindow_value(window):
    try:
        target_folder = CONFIG['TARGET_WINDOW']
        window['-TARGET WINDOW-'].update(target_folder)
    except:
        pass


def targetWindow_event(window, values):
    global CONFIG
    window_title = values['-WINDOW TITLES-']
    CONFIG['TARGET_WINDOW'] = window_title
    window['-TARGET WINDOW-'].update(window_title)
    window['-WINDOW TITLES-'].update(['Unused', get_titles()])


def targetFolder_value(window, values):
    try:
        target_folder = CONFIG['TARGET_FOLDER']
        window['-TARGET FOLDER-'].update(target_folder)
    except:
        pass


def targetFolder_event(values):
    global CONFIG
    CONFIG['TARGET_FOLDER'] = values['-TARGET FOLDER-']


def streaming_event(window, values):
    try:
        wincap = WindowCapture(values['-TARGET WINDOW-'])
        stream = wincap.get_screenshot()
    except:
        return
    stream_data = output_stream(stream, CONFIG['WINDOW_SIZE'])
    window['-VIDEO STREAM-'].update(data=stream_data)


def clear_event(window):
    global CONFIG, FIRST_LOAD
    FIRST_LOAD = False
    try:
        del CONFIG['TARGET_FOLDER']
    except:
        pass
    try:
        del CONFIG['TARGET_WINDOW']
    except:
        pass
    window['-TARGET FOLDER-'].update('')
    window['-TARGET WINDOW-'].update('')
    window['-VIDEO STREAM-'].update(
        data=resize_image(CONFIG['DISCONNECT_INFO'], CONFIG['WINDOW_SIZE']))


CONFIG = init_config()
STREAMING = True
DETECTING = False
FIRST_LOAD = True


def main():
    layout_props = [
        get_titles(),
        CONFIG['DISCONNECT_INFO'],
        CONFIG['WINDOW_SIZE']
    ]
    window = sg.Window('AI Bot', layout=layout_all(
        *layout_props), size=(1120, 630))
    timeout = int(1000/CONFIG['FPS'])

    while True:
        event, values = window.read(timeout=timeout)

        if event == sg.WIN_CLOSED:
            break

        if FIRST_LOAD:
            if values['-TARGET FOLDER-'] == '':
                targetFolder_value(window, values)
            if values['-TARGET WINDOW-'] == '':
                targetWindow_value(window)

        if event == '-TARGET FOLDER-':
            targetFolder_event(values)
        if event == '-WINDOW TITLES-':
            targetWindow_event(window, values)

        if event == '-START-':
            start_event(values)
        if event == '-PAUSE-':
            pause_event()

        if STREAMING:
            streaming_event(window, values)

        if event == '-CLEAR-':
            clear_event(window)

    init_config(conf_file=CONFIG)
    window.close()


if __name__ == '__main__':
    main()
