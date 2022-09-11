from imageai.Detection.Custom import CustomObjectDetection
from wincapture import WindowCapture
from components import layout_all
from utils import (
    resize_image,
    init_config,
    output_stream,
    get_titles,
    get_file_path,
    get_perm
)

import PySimpleGUI as sg


def start_event(window):
    global STREAMING, DETECTING, CHECKED
    STREAMING = True
    DETECTING = not DETECTING
    CHECKED = not CHECKED


def pause_event(window):
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


def targetFolder_value(window):
    try:
        target_folder = CONFIG['TARGET_FOLDER']
        window['-TARGET FOLDER-'].update(target_folder)
    except:
        pass


def targetFolder_event(values):
    global CONFIG
    CONFIG['TARGET_FOLDER'] = values['-TARGET FOLDER-']


def actions_value(window):
    try:
        actions = CONFIG['ACTIONS_LOGS']
        window['-ACTIONS LOGS-'].update(actions)
    except:
        pass


def speech_value(window):
    try:
        speech = CONFIG['SPEECH_LOGS']
        window['-SPEECH LOGS-'].update(speech)
    except:
        pass


def streaming_event(window, values, detector):
    try:
        wincap = WindowCapture(values['-TARGET WINDOW-'])
        stream = wincap.get_screenshot()
    except:
        return
    stream_data = output_stream(
        stream, CONFIG['WINDOW_SIZE'], detector, detecting=DETECTING)
    window['-VIDEO STREAM-'].update(data=stream_data)


def actions_logs_event(window, values):
    try:
        wincap = WindowCapture(values['-TARGET WINDOW-'])
        stream = wincap.get_screenshot()
    except:
        return
    stream_data = output_stream(stream, CONFIG['WINDOW_SIZE'])
    window['-VIDEO STREAM-'].update(data=stream_data)


def speeching_logs_event(window, values):
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
    window['-START-'].update(disabled=True)
    window['-TARGET FOLDER-'].update('')
    window['-TARGET WINDOW-'].update('')
    window['-VIDEO STREAM-'].update(
        data=resize_image(CONFIG['DISCONNECT_INFO'], CONFIG['WINDOW_SIZE']))
    window['-ACTIONS LOGS-'].update('')
    window['-SPEECH LOGS-'].update('')


def program_close():
    global CONFIG
    CONFIG['ACTIONS_LOGS'] = VALUES['-ACTIONS LOGS-']
    CONFIG['SPEECH_LOGS'] = VALUES['-SPEECH LOGS-']
    CONFIG['TARGET_WINDOW'] = VALUES['-TARGET WINDOW-']
    CONFIG['TARGET_FOLDER'] = VALUES['-TARGET FOLDER-']


def get_window_settings():
    layout_props = [
        get_titles(),
        CONFIG['DISCONNECT_INFO'],
        CONFIG['WINDOW_SIZE']
    ]
    main_settings = dict(
        layout=layout_all(*layout_props),
        size=(1120, 630)
    )

    icon_path = get_file_path(CONFIG['WINDOW_ICON'])
    if icon_path is not None:
        main_settings.update(icon=icon_path)

    return main_settings


def check_event(window, values):
    global DETECTING, CHECKED
    target_folder = values['-TARGET FOLDER-']
    perm_file = CONFIG['PERMISSION_FILE']
    if not get_perm(perm_file, target_folder, window, values):
        sg.Popup('WARNING!\n"target" or "window" is not ready',
                 title='CHECK ERROR')
    else:
        CHECKED = True


def init_detector():
    detector = CustomObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(
        "./mobs/models/detection_model-ex-049--loss-0012.515.h5")
    detector.setJsonPath("./mobs/json/detection_config.json")
    detector.loadModel()
    return detector


CONFIG = init_config()
STREAMING = True
DETECTING = False
FIRST_LOAD = True
VALUES = None
CHECKED = False


def main():
    global VALUES
    detector = init_detector()
    main_settings = get_window_settings()
    window = sg.Window('AI Bot', **main_settings)
    timeout = int(1000/CONFIG['FPS'])

    while True:
        event, values = window.read(timeout=timeout)

        if event == sg.WIN_CLOSED:
            program_close()
            init_config(conf_file=CONFIG)
            break

        if FIRST_LOAD:
            if values['-TARGET FOLDER-'] == '':
                targetFolder_value(window)
            if values['-TARGET WINDOW-'] == '':
                targetWindow_value(window)
            if values['-ACTIONS LOGS-'] == '':
                actions_value(window)
            if values['-SPEECH LOGS-'] == '':
                speech_value(window)

        if values['-TARGET WINDOW-'] != '':
            window['-PAUSE-'].update(disabled=False)
        else:
            window['-PAUSE-'].update(disabled=True)

        if event == '-TARGET FOLDER-':
            targetFolder_event(values)
        if event == '-WINDOW TITLES-':
            targetWindow_event(window, values)

        if event == '-START-':
            start_event(window)
        if event == '-PAUSE-':
            pause_event(window)

        if STREAMING:
            streaming_event(window, values, detector)
            # actions_logs_event(window, values)
            # speeching_logs_event(window, values)

        if event == '-CLEAR-':
            clear_event(window)

        if event == '-CHECK-':
            check_event(window, values)

        VALUES = {**values}

    window.close()


if __name__ == '__main__':
    main()
