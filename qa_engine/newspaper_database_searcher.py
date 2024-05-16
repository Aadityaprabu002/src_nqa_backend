import chromadb

from langchain_community.document_loaders import JSONLoader
from langchain_community.vectorstores import Chroma
from app_config import config
from util.progress_bar import ProgressBar
from newspaper_database_connection import NewspaperDatabaseConnectionAndContext


class NewspaperDatabaseSearcher:
    def __init__(
        self,
        ndbcc: NewspaperDatabaseConnectionAndContext,
    ) -> None:

        self.__langchain_chroma_client = ndbcc.get_langchain_chroma_client()
        print("NewspaperDatabaseSearcher initialized successfully.")

    def search(self, query: str, top_k: int = 5):
        progress_bar = ProgressBar(1, "Searching")
        search_results = self.__langchain_chroma_client.similarity_search(
            query=query, k=top_k
        )
        progress_bar.update()
        progress_bar.complete()
        return search_results
