import sys

sys.path.append("../trained_model")
sys.path.append("../model")
from trained_model import YoloV8NewspaperAllClass
from model import NewspaperComponent, RectangleCoordinate
from typing import List, Dict
import numpy as np
import cv2
from progress_bar import ProgressBar


class NewspaperAllClassImageSegmentor:
    AD = 0
    ARTICLE = 1

    def __init__(self) -> None:
        self.model = YoloV8NewspaperAllClass()
        print("NewspaperAllClassImageSegmentor initialized successfully.")

    def __convert_list_from_tensor_to_int(
        self, tensor_list: List[np.ndarray]
    ) -> List[int]:
        return [int(tensor) for tensor in tensor_list]

    def __segment(
        self,
        image: np.ndarray,
        target_class_id: int,
    ) -> List[NewspaperComponent]:

        image_copy = image.copy()

        result = self.model.predict(image)

        predicted_bboxes_xyxy_list = list(result[0].boxes.xyxy)
        predicted_class_id_list = list(result[0].boxes.cls)

        newspaper_component_list = []
        progress_bar = ProgressBar(
            len(predicted_class_id_list), "Segmenting components"
        )

        for i in range(len(predicted_class_id_list)):
            progress_bar.update()
            current_class_id = int(predicted_class_id_list[i].item())

            if current_class_id == target_class_id:

                current_class_bbox_xyxy = self.__convert_list_from_tensor_to_int(
                    predicted_bboxes_xyxy_list[i]
                )

                current_class_bbox_xyxy = RectangleCoordinate(current_class_bbox_xyxy)

                newspaper_component = NewspaperComponent(
                    newspaper_image=image,
                    component_class_id=current_class_id,
                    component_coordinate=current_class_bbox_xyxy,
                )

                newspaper_component_list.append(newspaper_component)
        progress_bar.complete()
        return newspaper_component_list

    def segment_article(self, image: np.ndarray):
        return self.__segment(image, self.ARTICLE)

    def segment_ad(self, image: np.ndarray):
        return self.__segment(image, self.AD)
