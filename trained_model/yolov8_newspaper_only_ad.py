from ultralytics import YOLO
import package_config
import numpy as np


class YoloV8NewspaperOnlyAd:
    def __init__(self) -> None:
        self.__model_path = package_config.config["YoloV8NewspaperOnlyAd"]
        self.__model = YOLO(self.__model_path)
        self.class_map = dict(self.__model.names)
        print("YoloV8NewspaperOnlyAd model loaded successfully.")

    def predict(self, image: np.ndarray):
        return self.__model.predict(source=image, verbose=False)
