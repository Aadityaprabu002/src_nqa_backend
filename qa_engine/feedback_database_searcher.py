import chromadb

from langchain_community.document_loaders import JSONLoader
from langchain_community.vectorstores import Chroma
from app_config import config
from util.progress_bar import ProgressBar
from feedback_database_connection import FeedbackDatabaseConnectionAndContext


class FeedbackDatabaseSearcher:
    def __init__(
        self,
        fdbcc: FeedbackDatabaseConnectionAndContext,
    ) -> None:

        self.__langchain_chroma_client = fdbcc.get_langchain_chroma_client()
        print("FeedbackDatabaseSearcher initialized successfully.")

    def search(self, query: str, top_k: int = 5):
        progress_bar = ProgressBar(1, "Searching")
        documents = self.__langchain_chroma_client.similarity_search(
            query=query, k=top_k
        )
        progress_bar.update()
        progress_bar.complete()
        return documents
