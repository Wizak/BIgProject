from utils import resize_image

import PySimpleGUI as sg


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
            sg.Button(button_text='START', enable_events=True, key='-START-'),
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
            sg.Image(source=resize_image(image_path, image_size), size=image_size, enable_events=True,
                     key='-VIDEO STREAM-')
        ]
    ]
    with open('test.txt', 'r') as file:
        text = file.read()
    center_column_right = [
        [
            sg.Multiline(default_text=text, size=(55, 22), key='-SPEECH LOGS-', autoscroll=True, disabled=True,
                         enable_events=True)
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
    layout = [
        [sg.Frame(layout=header_layout, title='',
                  element_justification='center', expand_x=True)],
        [sg.Frame(layout=center_layout, title='',
                  element_justification='center', expand_x=True)]
    ]
    return layout
