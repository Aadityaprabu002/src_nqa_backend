from app_config import config
from util.progress_bar import ProgressBar
from feedback_database_connection_and_context import (
    FeedbackDatabaseConnectionAndContext,
)
import json
import uuid


class FeedbackDatabaseIndexer:
    __RELEVANT = 1
    __IRRELEVANT = 0

    def __init__(self, fdbcc: FeedbackDatabaseConnectionAndContext) -> None:
        self.__collection = fdbcc.get_feedback_collection()
        self.__sqlite3_connection = fdbcc.get_sqlite3_connection()
        self.__sqlite3_cursor = fdbcc.get_sqlite3_cursor()

        print("FeedbackDatabaseIndexer initialized successfully.")

    def __insert_feedback(self, question_id, article_id_list):
        self.__sqlite3_cursor.execute(
            config["FeedbackDatabaseCommands"]["FeedbackTableInsert"],
            (
                question_id,
                json.dumps(article_id_list),
            ),
        )
        self.__sqlite3_connection.commit()

    def __update_feedback_file(
        self, question_id, question, article_id_list, relevancy_list
    ):

        l = len(relevancy_list)
        print(relevancy_list)
        score = 0
        for relevancy in relevancy_list:
            score += relevancy

        score = score / l
        info = ""
        path = config["FeedbackFilePath"]

        with open(path, "r") as file:
            info = json.load(file)

        data = {
            "question-id": question_id,
            "question": question,
            "score": score,
            "article-id-list": article_id_list,
            "relevancy-list": relevancy_list,
        }
        info.append(data)
        with open(path, "w") as file:
            json.dump(info, file)

    def add_feedback(self, question, article_id_list, relevancy_list):
        metadatas = []

        progress_bar = ProgressBar(3, "Indexing feedbacks")

        question_id = str(uuid.uuid4())

        self.__update_feedback_file(
            question_id, question, article_id_list, relevancy_list
        )
        progress_bar.update()

        relevant_article_id_list = []
        for i, relevancy in enumerate(relevancy_list):
            if relevancy == self.__RELEVANT:
                relevant_article_id_list.append(article_id_list[i])

        metadatas = {
            "question-id": question_id,
        }
        document = f"""{question}"""
        id = question_id

        progress_bar.update()
        self.__collection.add(documents=document, metadatas=metadatas, ids=id)

        progress_bar.update()
        self.__insert_feedback(question_id, relevant_article_id_list)

        progress_bar.complete()
