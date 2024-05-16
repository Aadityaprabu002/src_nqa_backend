import sys

sys.path.append("../trained_model")
sys.path.append("../model")
sys.path.append("../util")
from trained_model import YoloV8NewspaperOnlyArticle
from model import NewspaperComponent, RectangleCoordinate, ArticleComponent
from util.image_text_extractor import ImageTextExtractor
from typing import List, Dict
import numpy as np
import cv2
import os
from unidecode import unidecode
from progress_bar import ProgressBar
import uuid


class NewspaperOnlyArticleImageSegmentor:
    IGNORE = ["article-image-image", "article-image", "title"]

    def __init__(
        self,
        image_text_exractor: ImageTextExtractor,
    ) -> None:

        self.model = YoloV8NewspaperOnlyArticle()
        self.image_text_extractor = image_text_exractor
        print("NewspaperOnlyArticleImageSegmentor initialized successfully.")

    def __convert_list_from_tensor_to_int(
        self, tensor_list: List[np.ndarray]
    ) -> List[int]:
        return [int(tensor) for tensor in tensor_list]

    def __component_compare(self, component: ArticleComponent):
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
        progress_bar = ProgressBar(
            len(newspaper_component_list), "Segmenting all articles"
        )

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

                article_component = ArticleComponent(
                    article_image=image,
                    component_class_id=current_component_class_id,
                    component_coordinate=current_component_bbox,
                )

                prediction_map[current_component_name].append(article_component)

            predicted_results.append((image, prediction_map))

        progress_bar.complete()

        current_page_article_folder_path = f"{page_folder_path}/articles"
        os.makedirs(current_page_article_folder_path, exist_ok=True)

        info = dict()
        info["articles"] = list()

        progress_bar = ProgressBar(
            len(predicted_results), "Extracting all article contents"
        )

        for i in range(len(predicted_results)):
            progress_bar.update()
            predicted_result = predicted_results[i]

            prediction_map: Dict[str, List[ArticleComponent]] = predicted_result[1]

            current_article_folder_path = (
                f"{current_page_article_folder_path}/article{i+1}"
            )
            os.makedirs(current_article_folder_path, exist_ok=True)
            current_article_image_path = f"{current_article_folder_path}/image.jpg"

            cv2.imwrite(current_article_image_path, predicted_results[i][0])

            os.makedirs(current_article_folder_path, exist_ok=True)
            data = {
                "article-id": str(uuid.uuid4()),
                "article-image-path": current_article_image_path,
                "article-page-index": page_index,
                "article-author": "",
                "article-body": "",
                "article-title": "",
                "article-image-caption": "",
            }

            for (
                current_article_component_name,
                current_article_component,
            ) in prediction_map.items():

                if current_article_component_name in self.IGNORE:
                    continue

                # sort the components so that it is extracted in the correct order
                current_article_component.sort(key=self.__component_compare)

                content = ""

                for j in range(len(current_article_component)):
                    current_component_image = current_article_component[
                        j
                    ].crop_component_from_article_image()

                    current_component_image_text = self.image_text_extractor.extract(
                        current_component_image
                    )

                    content += " " + unidecode(current_component_image_text)

                data[current_article_component_name] = content

            if data["article-title"] == "" and data["article-body"] != "":

                data["article-title"] = data["article-body"]

            if data["article-title"] != "" and data["article-body"] == "":

                data["article-body"] = data["article-title"]

            info["articles"].append(data)

        progress_bar.complete()
        return info
