import chromadb
from langchain_community.vectorstores import Chroma
from app_config import config
from util.progress_bar import ProgressBar
from newspaper_database_connection import NewspaperDatabaseConnectionAndContext


class NewspaperDatabaseIndexer:
    def __init__(self, ndbcc: NewspaperDatabaseConnectionAndContext) -> None:
        self.__collection = ndbcc.get_newspaper_collection()
        print("NewspaperDatabaseIndexer initialized successfully.")
    
    def add_articles(self, articles):
        documents = []
        metadatas = []
        ids = []

        progress_bar = ProgressBar(len(articles) + 1, "Indexing articles")
        for article in articles:
            progress_bar.update()
            article_id = article["article-id"]
            article_image_path = article["article-image-path"]
            article_page_index = article["article-page-index"]
            article_author = article["article-author"]

            article_title = article["article-title"]
            article_body = article["article-body"]

            document = f"""
Title: {article_title}
Body: {article_body}
Author: {article_author}
"""
            metadata = {
                "article-image-path": article_image_path,
                "article-page-index": article_page_index,
                "article-id": article_id,
            }

            id = article_id

            documents.append(document)
            metadatas.append(metadata)
            ids.append(id)

        progress_bar.update()
        self.__collection.add(documents=documents, metadatas=metadatas, ids=ids)
        progress_bar.complete()
