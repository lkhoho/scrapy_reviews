# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BasicReviewItem(scrapy.Item):
    """ Review containing author, date, title, content. """

    def __init__(self):
        super().__init__()
        self["author"] = ""
        self["date"] = ""
        self["title"] = ""
        self["content"] = ""

    author = scrapy.Field()
    date = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()


class KBBReviewItem(BasicReviewItem):
    """ KBB review info. """

    def __init__(self):
        super().__init__()
        self["owned_mileage"] = 0
        self["pros"] = ""
        self["cons"] = ""
        self["recommend_count"] = 0
        self["helpful_count"] = "0/0"
        self["ratings_overall"] = 0
        self["ratings_value"] = 0
        self["ratings_reliability"] = 0
        self["ratings_quality"] = 0
        self["ratings_performance"] = 0
        self["ratings_styling"] = 0
        self["ratings_comfort"] = 0

    @staticmethod
    def headers() -> list:
        return [
            "author", "date", "title", "owned_mileage", "recommend_count",
            "helpful_count", "pros", "cons", "ratings_overall", "ratings_value",
            "ratings_reliability", "ratings_quality", "ratings_performance", "ratings_styling", "ratings_comfort"
        ]

    owned_mileage = scrapy.Field()
    pros = scrapy.Field()
    cons = scrapy.Field()
    recommend_count = scrapy.Field()
    helpful_count = scrapy.Field()
    ratings_overall = scrapy.Field()
    ratings_value = scrapy.Field()
    ratings_reliability = scrapy.Field()
    ratings_quality = scrapy.Field()
    ratings_performance = scrapy.Field()
    ratings_styling = scrapy.Field()
    ratings_comfort = scrapy.Field()


class EdmundsReviewItem(BasicReviewItem):
    """ Edmunds review info. """

    def __init__(self):
        super().__init__()
        self["score"] = 0
        self["vehicle_type"] = ""
        self["helpful_count"] = "0/0"
        self["recommend_up_count"] = 0
        self["recommend_down_count"] = 0
        self["best_features"] = []
        self["worst_features"] = []
        self["ratings_safety"] = 0
        self["ratings_performance"] = 0
        self["ratings_comfort"] = 0
        self["ratings_technology"] = 0
        self["ratings_interior"] = 0
        self["ratings_reliability"] = 0
        self["ratings_value"] = 0

    @staticmethod
    def headers() -> list:
        return [
            "author", "date", "title", "score", "vehicle_type",
            "helpful_count", "recommend_up_count", "recommend_down_count", "best_features", "worst_features",
            "ratings_safety", "ratings_performance", "ratings_comfort", "ratings_technology", "ratings_interior",
            "ratings_reliability", "ratings_value"
        ]

    score = scrapy.Field()
    vehicle_type = scrapy.Field()
    helpful_count = scrapy.Field()
    recommend_up_count = scrapy.Field()
    recommend_down_count = scrapy.Field()
    best_features = scrapy.Field()
    worst_features = scrapy.Field()
    ratings_safety = scrapy.Field()
    ratings_performance = scrapy.Field()
    ratings_comfort = scrapy.Field()
    ratings_technology = scrapy.Field()
    ratings_interior = scrapy.Field()
    ratings_reliability = scrapy.Field()
    ratings_value = scrapy.Field()


class OrbitzReviewItem(BasicReviewItem):
    """ Orbitz hotel review info. """

    def __init__(self):
        super().__init__()
        self["score"] = 0
        self["recommend_for"] = ""
        self["location"] = ""
        self["remark_pros"] = ""
        self["remark_cons"] = ""
        self["remark_location"] = ""
        self["response_title"] = ""
        self["response_author"] = ""
        self["response_date"] = ""
        self["response_content"] = ""

    @staticmethod
    def headers() -> list:
        return [
            "author", "date", "title", "score", "location",
            "recommend_for", "remark_pros", "remark_cons", "remark_location", "response_title",
            "response_author", "response_date", "response_content"
        ]

    score = scrapy.Field()
    recommend_for = scrapy.Field()
    location = scrapy.Field()
    remark_pros = scrapy.Field()
    remark_cons = scrapy.Field()
    remark_location = scrapy.Field()
    response_title = scrapy.Field()
    response_author = scrapy.Field()
    response_date = scrapy.Field()
    response_content = scrapy.Field()
