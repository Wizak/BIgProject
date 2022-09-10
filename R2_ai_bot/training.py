from imageai.Detection.Custom import DetectionModelTrainer


trainer = DetectionModelTrainer()
trainer.setModelTypeAsYOLOv3()
trainer.setDataDirectory(data_directory="mobs")
trainer.setTrainConfig(
    object_names_array=["mobs"], 
    batch_size=4, 
    num_experiments=20, 
    train_from_pretrained_model="models/pretrained-yolov3.h5")
trainer.trainModel()