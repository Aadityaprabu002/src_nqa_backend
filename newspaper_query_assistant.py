import sys

sys.path.append("./model")
sys.path.append("./util")
sys.path.append("./trained_model")
sys.path.append("./qa_engine")

from qa_engine import *
from trained_model import *
from util import *
import cv2
import os
from app_config import config
import json


class NewspaperQueryAssistant:
    SUB_CLASS_COUNT = 2

    def __init__(self) -> None:

        self.newspaper_database_connection_and_context = (
            NewspaperDatabaseConnectionAndContext()
        )
        self.newspaper_database_indexer = NewspaperDatabaseIndexer(
            self.newspaper_database_connection_and_context
        )
        self.newspaper_database_searcher = NewspaperDatabaseSearcher(
            self.newspaper_database_connection_and_context
        )
        self.newspaper_question_answerer = NewspaperQuestionAnswerer()

        self.image_text_extractor = ImageTextExtractor()

        self.pdf_transmuter = PdfTransmuter()

        self.newspaper_all_class_image_segmentor = NewspaperAllClassImageSegmentor()
        self.newspaper_only_article_image_segmentor = (
            NewspaperOnlyArticleImageSegmentor(self.image_text_extractor)
        )

        self.newspaper_only_ad_image_segmentor = NewspaperOnlyAdImageSegmentor(
            self.image_text_extractor
        )
        self.info_consolidator = InfoConsolidator()

        self.newspaper_info = {"articles": [], "ads": []}

        self.feedback_database_connection_and_context = (
            FeedbackDatabaseConnectionAndContext()
        )
        self.feedback_database_indexer = FeedbackDatabaseIndexer(
            self.feedback_database_connection_and_context
        )
        self.feedback_database_searcher = FeedbackDatabaseSearcher(
            self.feedback_database_connection_and_context
        )

        print("NewspaperQueryAssistant initialized successfully.")

    def __save_info(self, page_folder_path, page_info):
        save_path = f"{page_folder_path}/info.json"
        with open(save_path, "w") as file:
            page_info = json.dumps(page_info)
            file.write(page_info)

    def __save_newspaper_info(self, predict_folder_path):
        save_path = f"{predict_folder_path}/newspaper_info.json"
        with open(save_path, "w") as file:
            newspaper_info = json.dumps(self.newspaper_info)
            file.write(newspaper_info)

    def __transmute_pdf(self, pdf_path, predict_folder_path):
        self.pdf_transmuter.transmute(pdf_path, predict_folder_path)

    # def __process_context(self, predict_folder_path):
    #     self.context_searcher.process_context(predict_folder_path)

    # def __correct_info(self, current_page_folder_path, page_info):
    #     self.context_resolver.resolve(current_page_folder_path, page_info)

    def __setup_qa(self, current_predict_folder_path):
        print("Setting up QA")
        self.__save_newspaper_info(current_predict_folder_path)
        self.newspaper_database_indexer.add_articles(self.newspaper_info["articles"])

    def load_newspaper_database(self, predict_folder_name):
        current_predict_folder_path = (
            f"{config['RootOutputPath']}/{predict_folder_name}"
        )
        try:

            with open(
                f"{current_predict_folder_path}/newspaper_info.json", "r"
            ) as file:
                self.newspaper_info = dict(json.load(file))

            self.newspaper_database_indexer.add_articles(
                self.newspaper_info["articles"]
            )

        except:
            return False
        return True

    def process_pdf(self, pdf_path):
        root_output_folder_path = config["RootOutputPath"]
        current_predict_folder_name = (
            f"predict{len(os.listdir(root_output_folder_path)) + 1}"
        )
        current_predict_folder_path = (
            f"{root_output_folder_path}/{current_predict_folder_name}"
        )
        os.makedirs(current_predict_folder_path, exist_ok=True)
        self.__transmute_pdf(pdf_path, current_predict_folder_path)
        # self.__process_context(current_predict_folder_path)

        for page_index, current_page_folder_name in enumerate(
            os.listdir(current_predict_folder_path)
        ):
            current_page_folder_path = (
                f"{current_predict_folder_path}/{current_page_folder_name}"
            )
            image = cv2.imread(f"{current_page_folder_path}/image.png")
            print("Page:", page_index + 1)
            segmented_articles = (
                self.newspaper_all_class_image_segmentor.segment_article(image)
            )
            # segmented_ads = self.newspaper_all_class_image_segmentor.segment_ad(image)
            current_page_newspaper_component_list = {
                "articles": segmented_articles,
                # "ads": segmented_ads,
            }

            page_info = dict()

            page_article_info = self.newspaper_only_article_image_segmentor.segment(
                current_page_newspaper_component_list["articles"],
                current_page_folder_path,
                page_index + 1,
            )
            page_info["articles"] = page_article_info["articles"]

            # page_ad_info = self.newspaper_only_ad_image_segmentor.segment(
            #     current_page_newspaper_component_list["ads"],
            #     current_page_folder_path,
            #     page_index + 1,
            # )
            # page_info["ads"] = page_ad_info['ads']
            # self.__correct_info(current_page_folder_path)

            self.__save_info(current_page_folder_path, page_info)

            self.info_consolidator.append_articles(
                self.newspaper_info, page_info["articles"]
            )

            # self.info_consolidator.append_ads(self.newspaper_info, page_info["ads"])

        self.__setup_qa(current_predict_folder_path)

    def show(self, question):
        documents = self.newspaper_database_searcher.search(question)
        return documents

    def feedback_search(self, question):
        documents = self.feedback_database_searcher.search(question)
        return documents

    def answer(self, question):

        documents = self.show(question)
        answers = []
        for document in documents:
            answer = self.newspaper_question_answerer.extract_answer(question, document)
            answers.append(answer)

        return answers, documents

    def add_feedback(self, question, relevancy_list, article_id_list):
        feedback = {
            "question": question,
            "relevancy-list": relevancy_list,
            "article-id-list": article_id_list,
        }
        self.feedback_database_indexer.add_feedback(feedback)
