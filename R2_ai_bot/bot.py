import pyautogui
import time
import numpy

from imageai.Detection.Custom import CustomObjectDetection


def check_game_focus(title):
    try:
        return title in pyautogui.getActiveWindowTitle()
    except TypeError:
        pass


def get_game_position():
    id='control/window_id.png'
    try:
        location = list(pyautogui.locateOnScreen(id)[:2])
    except TypeError:
        pass
    else:
        corrected_location = location[0] - 102, location[1]
        return corrected_location


def get_game_screen():
    resolution= 1024, 768
    window = 'control/window.png'
    location = get_game_position()
    if location is not None:
        rectangle = location + resolution
        screen = pyautogui.screenshot(window, region=rectangle)
        return screen


def detection(frame, perscent):
    if frame is not None:
        pyautogui.keyDown('f')
        detector = CustomObjectDetection()
        detector.setModelTypeAsYOLOv3()
        detector.setModelPath("mobs/models/detection_model-ex-049--loss-0012.515.h5")
        detector.setJsonPath("mobs/json/detection_config.json")
        detector.loadModel()
        detections = detector.detectObjectsFromImage(
            input_image='control/window.png', 
            output_type='array', 
            minimum_percentage_probability=perscent)
        pyautogui.keyUp('f')
        return detections
    

def mob_looted():
    print('LOOT')
    pyautogui.keyDown('f')
    for _ in range(10):
        pyautogui.keyDown('e')
        pyautogui.keyUp('e')
    pyautogui.keyUp('f')


def mob_focus(x, y):
    print('ATACK')
    error = 0
    pyautogui.mouseDown(x, y, button='left')
    pyautogui.mouseDown(button='right')
    pyautogui.mouseUp(button='right')
    pyautogui.mouseUp(button='left')
    while 1:
        if pyautogui.locateOnScreen('control/mob_id.png') is None:
            if error:
                break
            else:
                pyautogui.keyDown('f')
                pyautogui.mouseUp(button='right')
                pyautogui.mouseUp(button='left')
                pyautogui.keyUp('f')
                return None
        error = 1
    time.sleep(1)


def mob_process(mobs):
    if mobs:
        for mob in mobs:
            game_pos = get_game_position()
            x1, y1, x2, y2 = mob['box_points']
            center_x = game_pos[0] + x1 + int(abs(x1 - x2)/2)
            center_y = game_pos[1] + y1 + int(abs(y1 - y2)/2)
            mob_focus(center_x, center_y)
            mob_looted()
    else:
        print('TP')
        pyautogui.keyDown('q')
        pyautogui.keyUp('q')
    time.sleep(1)


if __name__ == '__main__':
    window_title = '??'
    model_perscent = 40
    while 1:
        if check_game_focus(window_title):
            time.sleep(1)
            game_frame = numpy.asarray(get_game_screen())
            mobs_info = detection(game_frame, model_perscent)[-1]
            mob_process(mobs_info)