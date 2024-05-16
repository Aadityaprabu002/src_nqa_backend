from rectangle_coordinate import RectangleCoordinate
import numpy as np


class ArticleComponent:
    def __init__(
        self,
        article_image: np.ndarray,
        component_class_id: int,
        component_coordinate: RectangleCoordinate,
    ):
        self.article_image = article_image
        self.component_class_id = component_class_id
        self.component_coordinate = component_coordinate

    def crop_component_from_article_image(self) -> np.ndarray:
        x1, y1, x2, y2 = self.component_coordinate.xyxy
        return self.article_image[y1:y2, x1:x2]
