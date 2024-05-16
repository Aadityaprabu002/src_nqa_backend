import cv2
import numpy as np


class ImageTuner:
    def ___gray_scale(self, image):
        return cv2.cvtColor(src=image, code=cv2.COLOR_BGR2GRAY)

    def __invert(self, image):
        return cv2.bitwise_not(src=image)

    def __adaptive_threshold(self, image):
        return cv2.adaptiveThreshold(
            src=self.gray_scale(image),
            maxValue=255,
            adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C,
            thresholdType=cv2.THRESH_BINARY,
            blockSize=3,
            C=5,
        )

    def __thin_font(self, image, kernel_shape, iteration):
        image = self.__invert(image)

        kernel = np.ones(shape=kernel_shape, dtype=np.uint8)

        image = cv2.erode(src=image, kernel=kernel, iterations=iteration)

        image = self.__invert(image)
        return image

    def tune(self, image, kernal_shape=(1, 1), iteration=150):
        image_thinned = self.__thin_font(image, kernal_shape, iteration)
        image_adpt_thresh = self.__adaptive_threshold(image_thinned)
        return image_adpt_thresh
