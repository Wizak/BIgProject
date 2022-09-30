from utils import resize_image, get_file_path, create_image

import PySimpleGUI as sg
import os


def get_video_banner(image_path, image_size):
    sources = dict()
    path = get_file_path(image_path)
    if os.path.exists(path):
        sources.update(source=resize_image(image_path, image_size))
    else:
        sources.update(source=create_image(image_size))
    return sources


def layout_all(windows_list, image_path, image_size):
    window_menu = ['Unused', windows_list]
    header_column_left = [
        [
            sg.FolderBrowse(button_text='Target',
                            target='-TARGET FOLDER-', size=(7, 1), enable_events=True),
            sg.Input(size=(70, 1), enable_events=True,
                     readonly=True, key='-TARGET FOLDER-'),
            sg.ButtonMenu('Window', window_menu, size=(
                7, 1), key='-WINDOW TITLES-'),
            sg.Input(size=(30, 1), enable_events=True,
                     readonly=True, key='-TARGET WINDOW-')
        ]
    ]
    header_column_right = [
        [
            sg.Button(button_text='START', enable_events=True,
                      key='-START-', disabled=True),
            sg.Button(button_text='PAUSE', enable_events=True, key='-PAUSE-'),
            sg.Button(button_text='CLEAR', enable_events=True, key='-CLEAR-')
        ]
    ]
    header_layout = [
        [
            sg.Column(header_column_left,
                      element_justification='left', expand_x=True),
            sg.Column(header_column_right,
                      element_justification='right', expand_x=True)
        ]
    ]
    center_column_left = [
        [
            sg.Image(**get_video_banner(image_path, image_size), size=image_size, enable_events=True,
                     key='-VIDEO STREAM-')
        ]
    ]
    multiline_menu = ['', ['Save']]
    center_column_right = [
        [
            sg.Multiline(size=(55, 22), key='-ACTIONS LOGS-', autoscroll=True, disabled=True,
                         enable_events=True, right_click_menu=multiline_menu)
        ]
    ]
    center_layout = [
        [
            sg.Column(center_column_left,
                      element_justification='left'),
            sg.Column(center_column_right,
                      element_justification='right', expand_x=True)
        ]
    ]
    GRAPH_WIDTH, GRAPH_HEIGHT = 120, 40

    def GraphColumn(name, key):
        layout = [
            [sg.Text(name, size=(18, 1), font=('Helvetica 8'), key=key+'TXT_')],
            [sg.Graph((GRAPH_WIDTH, GRAPH_HEIGHT),
                      (0, 0),
                      (GRAPH_WIDTH, 100),
                      background_color='black',
                      key=key+'GRAPH_')]]
        return sg.Col(layout, pad=(2, 2))
    dash_layout = [
        [GraphColumn('Net Out', '_NET_OUT_'),
         GraphColumn('Net In', '_NET_IN_'),
         GraphColumn('Disk Read', '_DISK_READ_')],
        [GraphColumn('Disk Write', '_DISK_WRITE_'),
         GraphColumn('CPU Usage', '_CPU_'),
         GraphColumn('Memory Usage', '_MEM_')],
    ]
    footer_column_left = [
        [
            sg.Column(dash_layout),
            sg.Column([
                [
                    sg.Button(button_text='CHECK SETTINGS',
                              enable_events=True, key='-CHECK-', expand_x=True),
                    sg.Button(button_text='ACTIVATE BOT',
                              key='-ACTIVATE-', expand_x=True)
                ],
                [
                    sg.Button(button_text='SPEECH INTERVENE',
                              key='-SPEECH-', expand_x=True)
                ]
            ])
        ]
    ]
    footer_column_right = [
        [
            sg.Column([
                [sg.Multiline(size=(55, 18), key='-SPEECH LOGS-', autoscroll=True, disabled=True,
                              enable_events=True)]
            ])
        ]
    ]
    footer_layout = [
        [
            sg.Column(footer_column_left, element_justification='left',
                      expand_x=True, expand_y=True),
            sg.Column(footer_column_right,
                      element_justification='right', expand_x=True)
        ]
    ]
    layout = [
        [sg.Frame(layout=header_layout, title='',
                  element_justification='center', expand_x=True)],
        [sg.Frame(layout=center_layout, title='',
                  element_justification='center', expand_x=True)],
        [sg.Frame(layout=footer_layout, title='',
                  element_justification='center', expand_x=True)]
    ]
    return layout
