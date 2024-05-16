from langchain_community.vectorstores import Chroma
from app_config import config
from util.progress_bar import ProgressBar
from feedback_database_connection import FeedbackDatabaseConnectionAndContext
import json
import uuid


class FeedbackDatabaseIndexer:
    __RELEVANT = 1
    __IRRELEVANT = 0

    def __init__(self, fdbcc: FeedbackDatabaseConnectionAndContext) -> None:
        self.__collection = fdbcc.get_feedback_collection()
        print("FeedbackDatabaseIndexer initialized successfully.")

    def __update_feedback_file(
        self, question_id, question, article_id_list, relevancy_list
    ):
        l = len(relevancy_list)
        score = 0
        for relevancy in relevancy_list:
            score += relevancy

        score = score / l
        info = ""
        path = config["FeedbackDatabasePath"]

        with open(f"{path}/feedback.json", "r") as file:
            info = json.load(file)

        data = {
            "question-id": question_id,
            "question": question,
            "score": score,
            "article-id-list": article_id_list,
            "relevancy-list": relevancy_list,
        }
        info.append(data)
        with open(f"{path}/feedback.json", "w") as file:
            json.dump(info, file)

    def add_feedback(self, feedback):
        metadatas = []

        progress_bar = ProgressBar(2, "Indexing feedbacks")

        question_id = str(uuid.uuid4())
        question = feedback["question"]
        article_id_list = feedback["article-id-list"]
        relevancy_list = feedback["relevancy-list"]

        self.__update_feedback_file(
            question_id, question, article_id_list, relevancy_list
        )
        progress_bar.update()

        relevant_article_id_list = []
        for i, relevancy in enumerate(relevancy_list):
            if relevancy == self.__RELEVANT:
                relevant_article_id_list.append(article_id_list[i])

        metadatas = {
            "relevant-article-id-list": relevant_article_id_list,
            "question-id": question_id,
        }
        document = f"""{question}"""
        id = question_id

        progress_bar.update()
        self.__collection.add(documents=document, metadatas=metadatas, ids=id)
        progress_bar.complete()
