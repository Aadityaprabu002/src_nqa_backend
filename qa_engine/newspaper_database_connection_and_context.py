import chromadb
from chromadb.config import Settings
from app_config import config
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
import os
import json


class NewspaperDatabaseConnectionAndContext:
    def __init__(self) -> None:

        self.__settings = Settings()
        self.__settings.allow_reset = config["NewspaperDatabaseAllowReset"]
        self.__chroma_client = chromadb.PersistentClient(
            path=config["NewspaperDatabasePath"], settings=self.__settings
        )
        self.__reset()
        self.__collection = self.__chroma_client.get_or_create_collection(
            config["NewspaperDatabaseCollectionName"]
        )
        self.__embedding_function = SentenceTransformerEmbeddings(
            model_name=config["SentenceTransformerModel"]
        )
        self.__langchain_chroma_client = Chroma(
            embedding_function=self.__embedding_function,
            client=self.__chroma_client,
            collection_name=config["NewspaperDatabaseCollectionName"],
        )
        os.makedirs(config["RelevanceScorePath"], exist_ok=True)
        path = f"{config['RelevanceScorePath']}/relevance_score.json"
        with open(path, "w") as file:
            json.dump([], file)
        print("NewspaperDatabaseConnectionAndContext initialized successfully.")

    def __reset(self):
        self.__chroma_client.reset()
        print("NewspaperDatabaseConnectionAndContext reset successfully.")

    def get_newspaper_collection(self):
        return self.__collection

    def get_langchain_chroma_client(self):
        return self.__langchain_chroma_client

    def get_chroma_client(self):
        return self.__chroma_client
