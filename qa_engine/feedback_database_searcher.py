import chromadb
import json
from app_config import config
from util.progress_bar import ProgressBar
from feedback_database_connection_and_context import (
    FeedbackDatabaseConnectionAndContext,
)
from newspaper_database_connection_and_context import (
    NewspaperDatabaseConnectionAndContext,
)


class FeedbackDatabaseSearcher:
    def __init__(
        self,
        fdbcc: FeedbackDatabaseConnectionAndContext,
        ndbcc: NewspaperDatabaseConnectionAndContext,
    ) -> None:

        self.__langchain_chroma_client = fdbcc.get_langchain_chroma_client()
        self.__collection = ndbcc.get_newspaper_collection()
        self.__sqlite3_cursor = fdbcc.get_sqlite3_cursor()
        print("FeedbackDatabaseSearcher initialized successfully.")

    def search(self, query: str, top_k: int = 5):
        progress_bar = ProgressBar(1, "Searching")
        documents = self.__langchain_chroma_client.similarity_search(
            query=query, k=top_k
        )
        progress_bar.update()
        progress_bar.complete()
        return documents

    def fetch_info_about_related_articles(self, question_id):
        progress_bar = ProgressBar(1, "Fetching")
        info = {}
        try:
            row = self.__sqlite3_cursor.execute(
                config["FeedbackDatabaseCommands"][
                    "FeedbackTableFetchArticleIdListBasedOnQuestionIdLimitOne"
                ],
                (question_id,),
            )
            row = self.__sqlite3_cursor.fetchone()
            article_id_list = json.loads(row[0])
            info["related_articles_count"] = len(article_id_list)

        except Exception as e:
            print("Error:", e)
            print("Error while fetching article_id_list based on question_id")
            return []

        progress_bar.update()
        progress_bar.complete()
        return info

    def fetch_related_articles(self, question_id):
        progress_bar = ProgressBar(1, "Fetching")
        article_id_list = []
        try:
            self.__sqlite3_cursor.execute(
                config["FeedbackDatabaseCommands"][
                    "FeedbackTableFetchArticleIdListBasedOnQuestionIdLimitOne"
                ],
                (question_id,),
            )
            row = self.__sqlite3_cursor.fetchone()
            article_id_list = json.loads(row[0])

        except Exception as e:
            print("Error:", e)
            print("Error while fetching article_id_list based on question_id")
            return []

        result = self.__collection.get(ids=article_id_list)

        progress_bar.update()
        progress_bar.complete()
        return result
