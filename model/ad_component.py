from rectangle_coordinate import RectangleCoordinate
import numpy as np


class AdComponent:
    def __init__(
        self,
        ad_image: np.ndarray,
        component_class_id: int,
        component_coordinate: RectangleCoordinate,
    ):
        self.ad_image = ad_image
        self.component_class_id = component_class_id
        self.component_coordinate = component_coordinate

    def crop_component_from_ad_image(self) -> np.ndarray:
        x1, y1, x2, y2 = self.component_coordinate.xyxy
        return self.ad_image[y1:y2, x1:x2]
