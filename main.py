
import PySimpleGUI as sg
import tensorflow as tf
import os
import random

from imageai.Detection.Custom import CustomObjectDetection
from wincapture import WindowCapture
from components import layout_all
# from speech import recognition_speech
from datetime import datetime
from dashboard import *
from utils import (
    resize_image,
    init_config,
    output_stream,
    get_titles,
    get_file_path,
    get_perm
)


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'

tf.config.experimental.enable_mlir_graph_optimization()
tf.config.run_functions_eagerly(True)


def start_event(window):
    global STREAMING, DETECTING, CHECKED, DETECTOR_READY
    STREAMING = True
    DETECTING = not DETECTING
    CHECKED = not CHECKED


def pause_event(window):
    global STREAMING, DETECTING, DETECTOR_READY
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


def activate_game_bot(values):
    if 'R2' not in values['-TARGET WINDOW-'] or '??' not in values['-TARGET WINDOW-']:
        sg.Popup('WARNING!\ngame is not ready',
                 title='Activate ERROR')


def streaming_event(window, values, detector):
    global DETECTIONS
    try:
        wincap = WindowCapture(values['-TARGET WINDOW-'])
        stream = wincap.get_screenshot()
    except:
        return
    DETECTIONS, stream_data = output_stream(
        stream, CONFIG['WINDOW_SIZE'], detector, detecting=DETECTING)
    window['-VIDEO STREAM-'].update(data=stream_data)


def actions_logs_event(window, values):
    global DETECTOR_COUNT
    if DETECTING and DETECTIONS is not None:
        from datetime import datetime
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        if DETECTIONS != []:
            DETECTOR_COUNT += 1
            window["-ACTIONS LOGS-"].update('\n\n', append=True)
            window["-ACTIONS LOGS-"].update('Event ' + str(DETECTOR_COUNT), text_color_for_value='white',
                                            background_color_for_value='blue', append=True)
            window["-ACTIONS LOGS-"].update('-'*18, append=True)
            window["-ACTIONS LOGS-"].update(
                '--==DETECTED==--', text_color_for_value='yellow', background_color_for_value='black', append=True)
            window["-ACTIONS LOGS-"].update('-'*18, append=True)
            window["-ACTIONS LOGS-"].update(
                '[' + time + ']', text_color_for_value='white', background_color_for_value='blue', append=True)
            for idx, detect in enumerate(DETECTIONS):
                window["-ACTIONS LOGS-"].update('\n\n', append=True)
                window["-ACTIONS LOGS-"].update(f'{idx+1}. ', text_color_for_value='white',
                                                background_color_for_value='black', append=True)
                window["-ACTIONS LOGS-"].update('MONSTER => ' + detect['name'],
                                                text_color_for_value='black', background_color_for_value='yellow', append=True)
                window["-ACTIONS LOGS-"].update('\t', append=True)
                window["-ACTIONS LOGS-"].update('PROBABILITY => ' + str(round(detect['percentage_probability'], 3)),
                                                text_color_for_value='black', background_color_for_value='yellow', append=True)
                window["-ACTIONS LOGS-"].update('\n', append=True)
                window["-ACTIONS LOGS-"].update('POSITION => x = ' + str(detect['box_points'][0]) + ' y = ' + str(detect['box_points'][1]),
                                                text_color_for_value='black', background_color_for_value='yellow', append=True)


def speech_window():
    window = sg.Window('Speech Recognition', layout=[
                       [sg.Button('Hello World')]])
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
    window.close()


def speeching_logs_event(window, values):
    global DETECTOR_COUNT
    if DETECTING and DETECTIONS is not None:
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        commands = random.choices(
            SLAVE_MESSAGE['commands'], weights=SLAVE_MESSAGE['weights'], k=random.randint(1, 3))
        # time = '-===  DETECTED  ===-'
        if DETECTIONS != []:
            for command in commands:
                window["-SPEECH LOGS-"].update('\n', append=True)
                window["-SPEECH LOGS-"].update(command,
                                               text_color_for_value='black', background_color_for_value='yellow', append=True)


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


def save_actions_logs(values):
    with open('actions_logs.txt', 'w') as file:
        file.write(values['-ACTIONS LOGS-'])


def check_event(window, values):
    global DETECTING, CHECKED
    target_folder = values['-TARGET FOLDER-']
    perm_file = CONFIG['PERMISSION_FILE']
    if not get_perm(perm_file, target_folder, window, values):
        sg.Popup('WARNING!\n"target" or "window" is not ready',
                 title='CHECK ERROR')
    else:
        CHECKED = True


def init_detector(folder_path):
    model_path = os.path.join(
        folder_path, "models/detection_model-ex-049--loss-0012.515.h5")
    json_path = os.path.join(folder_path, "json/detection_config.json")
    detector = CustomObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(model_path)
    detector.setJsonPath(json_path)
    detector.loadModel()
    return detector


def psutility(window, net_graph_in, net_graph_out, disk_graph_read, gpu_usage_graph, cpu_usage_graph, mem_usage_graph):
    netio = psutil.net_io_counters()
    write_bytes = net_graph_out.graph_value(netio.bytes_sent)
    read_bytes = net_graph_in.graph_value(netio.bytes_recv)
    window['_NET_OUT_TXT_'].update(
        'Net out {}'.format(human_size(write_bytes)))
    window['_NET_IN_TXT_'].update(
        'Net In {}'.format(human_size(read_bytes)))
    # ----- Disk Graphs -----
    diskio = psutil.disk_io_counters()
    read_bytes = disk_graph_read.graph_value(diskio.read_bytes)
    window['_DISK_READ_TXT_'].update(
        'Disk Read {}'.format(human_size(read_bytes)))
    # ----- GPU Graph -----
    gpu = GPUtil.getGPUs()[-1].load*100
    gpu_usage_graph.graph_percentage_abs(gpu)
    window['_GPU_TXT_'].update('{0:2.0f}% GPU Used'.format(gpu))
    # ----- CPU Graph -----
    cpu = psutil.cpu_percent(0)
    cpu_usage_graph.graph_percentage_abs(cpu)
    window['_CPU_TXT_'].update('{0:2.0f}% CPU Used'.format(cpu))
    # ----- Memory Graph -----
    mem_used = psutil.virtual_memory().percent
    mem_usage_graph.graph_percentage_abs(mem_used)
    window['_MEM_TXT_'].update('{}% Memory Used'.format(mem_used))


CONFIG = init_config()
STREAMING = True
DETECTING = False
FIRST_LOAD = True
VALUES = None
CHECKED = False
DETECTIONS = None
DETECTOR_COUNT = 0
DETECTOR_READY = True

SLAVE_MESSAGE = {
    'commands': [
        '[ACTION] \tpress',
        '[ACTION] \tloot',
        '[MOVE] \tv',
        '[MOVE] \t^',
        '[MOVE] \t<-',
        '[MOVE] \t->',
        '[TARGET] \tvampire #1',
        '[TARGET] \tvampire #2',
        '[TARGET] \tvampire #3'
    ],
    'weights': [2, 2, 4, 3, 4, 3, 1, 1, 1]
}


def main():
    global VALUES, DETECTOR_READY
    detector = None
    main_settings = get_window_settings()
    window = sg.Window('AI Bot', **main_settings)
    timeout = int(1000/CONFIG['FPS'])

    netio = psutil.net_io_counters()
    net_in = window['_NET_IN_GRAPH_']
    net_graph_in = DashGraph(net_in, netio.bytes_recv, '#23a0a0')
    net_out = window['_NET_OUT_GRAPH_']
    net_graph_out = DashGraph(net_out, netio.bytes_sent, '#56d856')

    diskio = psutil.disk_io_counters()
    disk_graph_read = DashGraph(
        window['_DISK_READ_GRAPH_'], diskio.read_bytes, '#5681d8')

    gpu_usage_graph = DashGraph(window['_GPU_GRAPH_'], 0, '#d34545')
    cpu_usage_graph = DashGraph(window['_CPU_GRAPH_'], 0, '#d34545')
    mem_usage_graph = DashGraph(window['_MEM_GRAPH_'], 0, '#BE7C29')

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

        if CHECKED and DETECTOR_READY:
            detector = init_detector(values['-TARGET FOLDER-'])
            DETECTOR_READY = False

        if STREAMING:
            streaming_event(window, values, detector)
            actions_logs_event(window, values)
            speeching_logs_event(window, values)

        if event == '-CLEAR-':
            clear_event(window)

        if event == '-CHECK-':
            check_event(window, values)

        if event == '-ACTIVATE-':
            activate_game_bot(values)

        if event == '-SPEECH-':
            speech_window()

        if event == 'Save':
            save_actions_logs(values)

        psutility(window, net_graph_in, net_graph_out, disk_graph_read,
                  gpu_usage_graph, cpu_usage_graph, mem_usage_graph)

        VALUES = {**values}

    window.close()


if __name__ == '__main__':
    main()
