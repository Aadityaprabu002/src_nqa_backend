from pytesseract import pytesseract
from app_config import config

# Dont change the path, it is in relation to the newspaper_query_assistant.py file or root directory's file.
pytesseract.tesseract_cmd = config["OcrEnginePath"]


class ImageTextExtractor:
    def extract(self, image) -> str:
        return (
            pytesseract.image_to_string(image)
            .replace("-\n", "")
            .replace("\n", " ")
            .lower()
        )
