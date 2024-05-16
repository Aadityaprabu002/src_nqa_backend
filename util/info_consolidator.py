class InfoConsolidator:
    def append_articles(self, newspaper_info, articles):
        newspaper_info["articles"].extend(articles)

    def append_ads(self, newspaper_info, ads):
        newspaper_info["ads"].extend(ads)
