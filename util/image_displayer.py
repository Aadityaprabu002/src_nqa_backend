import cv2
import threading


class ImageDisplayer:

    def __display(self, title, image):

        cv2.imshow(title, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def display(self, title, image, reverse_scale=1.0):
        (h, w) = image.shape[:2]
        new_size = (int(w / reverse_scale), int(h / reverse_scale))
        resized_image = cv2.resize(image, new_size)
        thread = threading.Thread(
            target=self.__display,
            args=(
                title,
                resized_image,
            ),
        )
        thread.start()
