from rectangle_coordinate import RectangleCoordinate
import numpy as np


class NewspaperComponent:
    def __init__(
        self,
        newspaper_image: np.ndarray,
        component_class_id: int,
        component_coordinate: RectangleCoordinate,
    ):

        self.newspaper_image = newspaper_image
        self.component_class_id = component_class_id
        self.component_coordinate = component_coordinate

    def crop_component_from_newspaper_image(self) -> np.ndarray:
        x1, y1, x2, y2 = self.component_coordinate.xyxy
        return self.newspaper_image[y1:y2, x1:x2]
