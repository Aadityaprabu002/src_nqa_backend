import os
import json
from app_config import config


class NewspaperAnalyticsDatabase:
    def __init__(self) -> None:
        os.makedirs(config["AnalyticsDatabaseFolderPath"], exist_ok=True)
        self.is_busy = False

        self.__path = config["AnalyticsFilePath"]

        self.__template = {
            "article_category": {
                "business": 0,
                "entertainment": 0,
                "health": 0,
                "news": 0,
                "politics": 0,
                "sport": 0,
            },
            "newspaper_count": 0,
            "article_count": 0,
            "ad_count": 0,
        }

        if not os.path.exists(self.__path):
            with open(self.__path, "w") as file:
                json.dump(self.__template, file)

        print("NewspaperAnalyticsDatabaseConnection initialized successfully.")

    def __get_analytics_data(self):
        data = dict()
        with open(self.__path, "r") as file:
            data = dict(json.load(file))
        print(data.keys())
        return data

    def get_analytics_data(self):
        if self.is_busy:
            return {"error": "Database is busy"}
        return self.__get_analytics_data()

    def update_analytics_data(self, new_data):
        self.is_busy = True
        old_data = self.__get_analytics_data()

        updated_data = dict()

        updated_data["article_count"] = (
            old_data["article_count"] + new_data["articles_count"]
        )

        updated_data["ad_count"] = old_data["ad_count"] + new_data["ads_count"]
        updated_data["newspaper_count"] = (
            old_data["newspaper_count"] + new_data["newspaper_count"]
        )

        updated_data["article_category"] = {
            key: old_data["article_category"][key] + new_data["article_category"][key]
            for key in old_data["article_category"]
        }

        with open(self.__path, "w") as file:
            json.dump(updated_data, file)

        self.is_busy = False

    def get_analytics_template(self):
        return self.__template
