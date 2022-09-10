from imageai.Detection.Custom import CustomObjectDetection

detector = CustomObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath("mobs/models/detection_model-ex-049--loss-0012.515.h5")
detector.setJsonPath("mobs/json/detection_config.json")
detector.loadModel()
detections = detector.detectObjectsFromImage(
    input_image="test/mob.png", 
    output_image_path="test/mob-detected.png", 
    minimum_percentage_probability=40)

with open('test/detected.txt', 'w') as f:
    f.write(str(detections))