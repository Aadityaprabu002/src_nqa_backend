import chromadb
from chromadb.config import Settings
from app_config import config
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
import os
import json
import sqlite3
from util import ProgressBar


class FeedbackDatabaseConnectionAndContext:
    def __init__(self) -> None:
        os.makedirs(config["FeedbackDatabaseFolderPath"], exist_ok=True)

        path = f"""{config["FeedbackDatabaseFolderPath"]}/{config["FeedbackDatabaseFileName"]}"""

        self.__sqlite3_connection = sqlite3.connect(path)

        try:
            command = config["FeedbackDatabaseCommands"]["FeedbackTableDropIfExists"]
            cursor = self.__sqlite3_connection.cursor()
            cursor.execute(command)
            command = config["FeedbackDatabaseCommands"][
                "FeedbackTableCreateIfNotExist"
            ]
            cursor.execute(command)
            self.__sqlite3_connection.commit()
        except sqlite3.Error as er:
            print(er.sqlite_errorcode)  # Prints 275
            print(er.sqlite_errorname)
            os._exit(1)

        self.__settings = Settings()
        self.__settings.allow_reset = config["FeedbackDatabaseAllowReset"]
        self.__chroma_client = chromadb.PersistentClient(
            path=config["FeedbackDatabaseFolderPath"], settings=self.__settings
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

        path = config["FeedbackFilePath"]
        with open(path, "w") as file:
            json.dump([], file)

        print("FeedbackDatabaseConnectionAndContext initialized successfully.")

    def clear(self):
        def clear_folder(folder_path):
            for file_name in os.listdir(folder_path):
                if file_name in [
                    ".gitkeep",
                    "chroma.sqlite3",
                    "feedbacks.json",
                    "feedback.sqlite3",
                ]:
                    continue
                file_path = f"{folder_path}/{file_name}"
                if os.path.isdir(file_path):
                    clear_folder(file_path)
                else:
                    os.remove(file_path)
            if folder_path != config["FeedbackDatabaseFolderPath"]:
                os.rmdir(folder_path)

        path = config["FeedbackDatabaseFolderPath"]
        progress_bar = ProgressBar(2, "Clearing Feedback Database")
        progress_bar.update()
        clear_folder(path)
        progress_bar.update()

        progress_bar.complete()

        print("FeedbackDatabaseConnectionAndContext cleared successfully.")

    def __reset(self):
        self.__chroma_client.reset()
        print("FeedbackDatabaseConnectionAndContext reset successfully.")

    def get_feedback_collection(self):
        return self.__collection

    def get_langchain_chroma_client(self):
        return self.__langchain_chroma_client

    def get_chroma_client(self):
        return self.__chroma_client

    def get_sqlite3_connection(self):
        return self.__sqlite3_connection

    def get_sqlite3_cursor(self):
        return self.__sqlite3_connection.cursor()
