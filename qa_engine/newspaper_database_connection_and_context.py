import chromadb
from chromadb.config import Settings
from app_config import config
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
import os
import json
from util import ProgressBar


class NewspaperDatabaseConnectionAndContext:
    def __init__(self) -> None:

        self.__settings = Settings()
        self.__settings.allow_reset = config["NewspaperDatabaseAllowReset"]
        self.__chroma_client = chromadb.PersistentClient(
            path=config["NewspaperDatabaseFolderPath"], settings=self.__settings
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

        print("NewspaperDatabaseConnectionAndContext initialized successfully.")

    def clear(self):

        def clear_folder(folder_path):
            for file_name in os.listdir(folder_path):
                if file_name in [".gitkeep", "chroma.sqlite3"]:
                    continue
                file_path = f"{folder_path}/{file_name}"
                if os.path.isdir(file_path):
                    clear_folder(file_path)
                else:
                    os.remove(file_path)
            if folder_path != config["NewspaperDatabaseFolderPath"]:
                os.rmdir(folder_path)

        path = config["NewspaperDatabaseFolderPath"]
        progress_bar = ProgressBar(2, "Clearing Newspaper Database")
        progress_bar.update()
        clear_folder(path)

        progress_bar.update()
        progress_bar.complete()
        print("NewspaperDatabaseConnectionAndContext cleared successfully.")

    def __reset(self):
        self.__chroma_client.reset()
        print("NewspaperDatabaseConnectionAndContext reset successfully.")

    def get_newspaper_collection(self):
        return self.__collection

    def get_langchain_chroma_client(self):
        return self.__langchain_chroma_client

    def get_chroma_client(self):
        return self.__chroma_client
