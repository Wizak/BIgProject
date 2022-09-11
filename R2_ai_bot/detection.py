from imageai.Detection.Custom import CustomObjectDetection

import cv2


image = cv2.imread("test/mob.png")


detector = CustomObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(
    "../mobs/models/detection_model-ex-049--loss-0012.515.h5")
detector.setJsonPath("../mobs/json/detection_config.json")
detector.loadModel()
detections = detector.detectObjectsFromImage(
    input_image=image,
    input_type='array',
    output_type='array',
    minimum_percentage_probability=40,
    extract_detected_objects=True,
    thread_safe=False
)

# img = PIL.Image.fromarray(detections[0])
# img.save('test/mob-detected.png')

cv2.imwrite('test/mob-detected.png', detections[0])
with open('test/detected.txt', 'w') as f:
    f.write(str(detections))
