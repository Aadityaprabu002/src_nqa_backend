import sys

sys.path.append("../trained_model")
sys.path.append("../model")
sys.path.append("../util")
from trained_model import YoloV8NewspaperOnlyAd
from model import NewspaperComponent, RectangleCoordinate, AdComponent
from util.image_text_extractor import ImageTextExtractor
from typing import List, Dict
import numpy as np
import cv2
import os
from unidecode import unidecode
from progress_bar import ProgressBar
import uuid


class NewspaperOnlyAdImageSegmentor:
    IGNORE = ["ad"]

    def __init__(
        self,
        image_text_exractor: ImageTextExtractor,
    ) -> None:

        self.model = YoloV8NewspaperOnlyAd()
        self.image_text_extractor = image_text_exractor
        print("NewspaperOnlyAdImageSegmentor initialized successfully.")

    def __convert_list_from_tensor_to_int(
        self, tensor_list: List[np.ndarray]
    ) -> List[int]:
        return [int(tensor) for tensor in tensor_list]

    def __component_compare(self, component: AdComponent):
        """To compare the components as in which comes first based on top left coordinates"""
        x1, y1, _, _ = component.component_coordinate.xyxy
        return (x1, y1)

    def segment(
        self,
        newspaper_component_list: List[NewspaperComponent],
        page_folder_path,
        page_index,
    ):

        predicted_results = []
        progress_bar = ProgressBar(len(newspaper_component_list), "Segmenting all ads")
        for newspaper_component in newspaper_component_list:
            progress_bar.update()
            image = newspaper_component.crop_component_from_newspaper_image()

            result = self.model.predict(image)

            predicted_bboxes_xyxy = list(result[0].boxes.xyxy)
            predicted_class_id_list = list(result[0].boxes.cls)

            prediction_map = dict()

            for (
                component_class_id,
                component_name,
            ) in self.model.class_map.items():
                prediction_map[component_name] = list()

            for i in range(len(predicted_class_id_list)):
                current_component_class_id = int(predicted_class_id_list[i].item())
                current_component_name = self.model.class_map[
                    current_component_class_id
                ]

                current_component_bbox = self.__convert_list_from_tensor_to_int(
                    predicted_bboxes_xyxy[i]
                )

                current_component_bbox = RectangleCoordinate(current_component_bbox)

                ad_component = AdComponent(
                    ad_image=image,
                    component_class_id=current_component_class_id,
                    component_coordinate=current_component_bbox,
                )

                prediction_map[current_component_name].append(ad_component)

            predicted_results.append((image, prediction_map))

        progress_bar.complete()

        current_page_ad_folder_path = f"{page_folder_path}/ads"
        os.makedirs(current_page_ad_folder_path, exist_ok=True)

        info = dict()
        info["ads"] = list()

        progress_bar = ProgressBar(
            len(newspaper_component_list), "Extracting all ad contents"
        )

        for i in range(len(predicted_results)):
            predicted_result = predicted_results[i]

            prediction_map: Dict[str, List[AdComponent]] = predicted_result[1]

            current_ad_folder_path = f"{current_page_ad_folder_path}/ad{i+1}"
            os.makedirs(current_ad_folder_path, exist_ok=True)
            current_ad_image_path = f"{current_ad_folder_path}/image.jpg"

            cv2.imwrite(current_ad_image_path, predicted_results[i][0])

            os.makedirs(current_ad_folder_path, exist_ok=True)
            data = {
                "ad-id": str(uuid.uuid4()),
                "ad-page-index": page_index + 1,
                "ad-image-path": current_ad_image_path,
                "ad-highlight": "",
            }

            for (
                current_ad_component_name,
                current_ad_component,
            ) in prediction_map.items():

                if current_ad_component_name in self.IGNORE:
                    continue

                # sort the components so that it is extracted in the correct order
                current_ad_component.sort(key=self.__component_compare)

                content = ""
                for j in range(len(current_ad_component)):
                    current_component_image = current_ad_component[
                        j
                    ].crop_component_from_ad_image()

                    current_component_image_text = self.image_text_extractor.extract(
                        current_component_image
                    )

                    content += " " + unidecode(current_component_image_text)

                data[current_ad_component_name].append(content)

            info["ads"].append(data)

        progress_bar.update()
        return info
