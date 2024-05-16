import fitz
import os
from progress_bar import ProgressBar


class PdfTransmuter:
    def __to_pdf(self, pdf_document, page_folder_path, page_number):
        pdf = fitz.open()
        pdf.insert_pdf(pdf_document, from_page=page_number, to_page=page_number)
        pdf_file_path = f"{page_folder_path}/pdf.pdf"
        pdf.save(pdf_file_path)

    def __to_image(self, pdf_document, page_folder_path, page_number, image_dpi=300):
        page = pdf_document.load_page(page_number)
        image = page.get_pixmap(
            matrix=fitz.Matrix(1, 1).prescale(image_dpi / 72, image_dpi / 72)
        )
        image_path = f"{page_folder_path}/image.png"
        image.save(image_path)

    def transmute(self, pdf_path, predict_folder_path, image_dpi=300):

        pdf_document = fitz.open(pdf_path)
        proress_bar = ProgressBar(
            len(pdf_document), "Transmuting PDF to page wise images and PDFs"
        )

        for current_page_number in range(len(pdf_document)):
            proress_bar.update()
            current_page_folder_path = (
                f"{predict_folder_path}/page{current_page_number}"
            )
            os.makedirs(current_page_folder_path, exist_ok=True)
            # self.__to_pdf(pdf_document, current_page_folder_path, current_page_number)
            self.__to_image(pdf_document, current_page_folder_path, current_page_number)

        proress_bar.complete()
