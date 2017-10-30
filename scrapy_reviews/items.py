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

    @staticmethod
    def get_column_headers() -> list:
        return ["author", "date", "title"]

    def get_column_values(self) -> list:
        return [self["author"], self["date"], self["title"]]

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
        self["ratings"] = {
            "overall": 0,
            "value": 0,
            "reliability": 0,
            "quality": 0,
            "performance": 0,
            "styling": 0,
            "comfort": 0
        }

    @staticmethod
    def get_column_headers() -> list:
        return super(KBBReviewItem, KBBReviewItem).get_column_headers() + [
            "owned_mileage", "recommend_count", "helpful_count", "pros", "cons", "ratings_overall", "ratings_value",
            "ratings_reliability", "ratings_quality", "ratings_performance", "ratings_styling", "ratings_comfort"
        ]

    def get_column_values(self) -> list:
        return super().get_column_values() + [
            self["owned_mileage"], self["recommend_count"], self["helpful_count"], self["pros"], self["cons"],
            self["ratings"]["overall"], self["ratings"]["value"], self["ratings"]["reliability"],
            self["ratings"]["quality"], self["ratings"]["performance"], self["ratings"]["styling"],
            self["ratings"]["comfort"]
        ]

    owned_mileage = scrapy.Field()
    pros = scrapy.Field()
    cons = scrapy.Field()
    recommend_count = scrapy.Field()
    helpful_count = scrapy.Field()
    ratings = scrapy.Field()


class EdmundsReviewItem(BasicReviewItem):
    """ Edmunds review info. """

    def __init__(self):
        super().__init__()
        self["score"] = 0
        self["vehicle_type"] = ""
        self["helpful_count"] = "0/0"
        self["recommend_count"] = {"up": 0, "down": 0}
        self["best_features"] = []
        self["worst_features"] = []
        self["ratings"] = {
            "safety": 0,
            "performance": 0,
            "comfort": 0,
            "technology": 0,
            "interior": 0,
            "reliability": 0,
            "value": 0
        }

    @staticmethod
    def get_column_headers() -> list:
        return super(EdmundsReviewItem, EdmundsReviewItem).get_column_headers() + [
            "score", "vehicle_type", "helpful_count", "recommend_up_count", "recommend_down_count", "best_features",
            "worst_features", "ratings_safety", "ratings_performance", "ratings_comfort", "ratings_technology",
            "ratings_interior", "ratings_reliability", "ratings_value"
        ]

    def get_column_values(self) -> list:
        return super().get_column_values() + [
            self["score"], self["vehicle_type"], self["helpful_count"], self["recommend_count"]["up"],
            self["recommend_count"]["down"], self["best_features"], self["worst_features"], self["ratings"]["safety"],
            self["ratings"]["performance"], self["ratings"]["comfort"], self["ratings"]["technology"],
            self["ratings"]["interior"], self["ratings"]["reliability"], self["ratings"]["value"]
        ]

    score = scrapy.Field()
    vehicle_type = scrapy.Field()
    helpful_count = scrapy.Field()
    recommend_count = scrapy.Field()
    best_features = scrapy.Field()
    worst_features = scrapy.Field()
    ratings = scrapy.Field()


class OrbitzReviewItem(BasicReviewItem):
    """ Orbitz hotel review info. """

    def __init__(self):
        super().__init__()
        self["score"] = 0
        self["will_recommend"] = 0
        self["recommend_for"] = ""
        self["location"] = ""
        self["remark"] = {
            "pros": "",
            "cons": "",
            "location": ""
        }
        self["response"] = BasicReviewItem()

    @staticmethod
    def get_column_headers() -> list:
        return super(OrbitzReviewItem, OrbitzReviewItem).get_column_headers() + [
            "score", "location", "will_recommend", "recommend_for", "remark_pros", "remark_cons", "remark_location",
            "response_title", "response_author", "response_date", "response_content"
        ]

    def get_column_values(self) -> list:
        return super().get_column_values() + [
            self["score"], self["location"], self["will_recommend"], self["recommend_for"], self["remark"]["pros"],
            self["remark"]["cons"], self["remark"]["location"], self["response"]["title"], self["response"]["author"],
            self["response"]["date"], self["response"]["content"]
        ]

    score = scrapy.Field()
    will_recommend = scrapy.Field()
    recommend_for = scrapy.Field()
    location = scrapy.Field()
    remark = scrapy.Field()
    response = scrapy.Field()


class TripAdvisorReviewItem(BasicReviewItem):
    """ TripAdvisor restaurant review info. """

    def __init__(self):
        super().__init__()
        self["score"] = 0
        self["via_mobile"] = 0
        self["helpful_count"] = 0
        self["location"] = ""
        self["level"] = 0
        self["review_count"] = 0
        self["contribution_count"] = 0
        self["helpful_votes"] = 0

    @staticmethod
    def get_column_headers() -> list:
        return super(TripAdvisorReviewItem, TripAdvisorReviewItem).get_column_headers() + [
            "score", "helpful_count", "location", "level", "review_count", "contribution_count", "helpful_votes"
        ]

    def get_column_values(self) -> list:
        return super().get_column_values() + [
            self["score"], self["helpful_count"], self["location"], self["level"], self["review_count"],
            self["contribution_count"], self["helpful_votes"]
        ]

    score = scrapy.Field()
    via_mobile = scrapy.Field()
    helpful_count = scrapy.Field()
    location = scrapy.Field()
    level = scrapy.Field()
    review_count = scrapy.Field()
    contribution_count = scrapy.Field()
    helpful_votes = scrapy.Field()
