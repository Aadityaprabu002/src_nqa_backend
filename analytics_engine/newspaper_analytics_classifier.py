import json
from collections import defaultdict
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from app_config import config
from util.progress_bar import ProgressBar
from newspaper_analytics_database import NewspaperAnalyticsDatabase


class NewspaperAnalyticsClassifier:
    def __init__(
        self, newspaper_analytics_database: NewspaperAnalyticsDatabase
    ) -> None:
        self.__tokenizer = AutoTokenizer.from_pretrained(config["ClassifierModel"])
        self.__model = AutoModelForSequenceClassification.from_pretrained(
            config["ClassifierModel"]
        )
        self.__newspaper_analytics_database = newspaper_analytics_database
        self.__class_map = {
            i: label
            for i, label in enumerate(
                ["business", "entertainment", "health", "news", "politics", "sport"]
            )
        }

    def __classify(self, text):
        inputs = self.__tokenizer(
            text, padding=True, truncation=True, return_tensors="pt"
        )
        outputs = self.__model(**inputs)
        predicted_class = outputs.logits.argmax().item()
        return predicted_class

    def classify(self, path):

        data = []
        with open(path, "r") as file:
            data = dict(json.load(file))

        result = self.__newspaper_analytics_database.get_analytics_template()
        article_category_frequency = result["article_category"]
        progress_bar = ProgressBar(len(data["articles"]), "Classifying articles")
        for article in data["articles"]:
            progress_bar.update()
            text = article["article-title"] + " " + article["article-body"]
            predicted_category = self.__classify(text)
            article_category_frequency[self.__class_map[predicted_category]] += 1

        progress_bar.complete()

        result = {
            "articles_count": len(data["articles"]),
            "ads_count": len(data["ads"]),
            "article_category": dict(article_category_frequency),
            "newspaper_count": 1,
        }
        return result
