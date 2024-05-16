import chromadb
from chromadb.config import Settings
from app_config import config
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
import os
import json


class FeedbackDatabaseConnectionAndContext:
    def __init__(self) -> None:

        self.__settings = Settings()
        self.__settings.allow_reset = config["FeedbackDatabaseAllowReset"]
        self.__chroma_client = chromadb.PersistentClient(
            path=config["FeedbackDatabasePath"], settings=self.__settings
        )
        self.__reset()
        self.__collection = self.__chroma_client.get_or_create_collection(
            config["FeedbackDatabaseCollectionName"]
        )
        self.__embedding_function = SentenceTransformerEmbeddings(
            model_name=config["SentenceTransformerModel"]
        )
        self.__langchain_chroma_client = Chroma(
            embedding_function=self.__embedding_function,
            client=self.__chroma_client,
            collection_name=config["FeedbackDatabaseCollectionName"],
        )

        os.makedirs(config["FeedbackDatabasePath"], exist_ok=True)
        path = f"""{config["FeedbackDatabasePath"]}/feedback.json"""
        with open(path, "w") as file:
            json.dump([], file)

        print("FeedbackDatabaseConnectionAndContext initialized successfully.")

    def __reset(self):
        self.__chroma_client.reset()
        print("FeedbackDatabaseConnectionAndContext reset successfully.")

    def get_feedback_collection(self):
        return self.__collection

    def get_langchain_chroma_client(self):
        return self.__langchain_chroma_client

    def get_chroma_client(self):
        return self.__chroma_client
