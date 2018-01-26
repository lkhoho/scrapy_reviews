# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MongoDBItem(scrapy.Item):
    _id = scrapy.Field()
    scraped_date = scrapy.Field()
    tags = scrapy.Field()


class BasicReviewItem(scrapy.Item):
    """ Review containing author, date, title, content. """

    def __init__(self):
        super().__init__()
        self["author"] = ""
        self["date"] = ""
        self["title"] = ""
        self["content"] = ""

    @staticmethod
    def get_column_header_index(header: str) -> int:
        return BasicReviewItem.get_column_headers().index(header)

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


class BizRateReviewItem(BasicReviewItem, MongoDBItem):
    """ BizRate store review info. """

    def __init__(self):
        super().__init__()
        BizRateReviewItem.TITLE_INDEX = BasicReviewItem.get_column_header_index("title")
        self["overall_satisfaction"] = 0
        self["would_shop_here_again"] = 0
        self["likelihood_to_recommend"] = 0
        self["ratings_site_experience"] = {
            "ease_of_finding": -1,
            "design_site": -1,
            "satisfaction_checkout": -1,
            "product_selection": -1,
            "clarity_product_info": -1,
            "charges_stated_clearly": -1,
            "price_relative_other_retailers": -1,
            "shipping_charges": -1,
            "variety_shipping_options": -1
        }
        self["ratings_after_purchase"] = {
            "on_time_delivery": -1,
            "order_tracking": -1,
            "product_met_expectations": -1,
            "customer_support": -1,
            "product_availability": -1,
            "returns_process": -1
        }
        self["review_after_purchase"] = BasicReviewItem()

    @staticmethod
    def get_column_headers() -> list:
        headers = super(BizRateReviewItem, BizRateReviewItem).get_column_headers()
        del headers[BizRateReviewItem.TITLE_INDEX]  # remove 'title'
        return [("review_site_experience_" + header) for header in headers] + [
            "overall_satisfaction", "would_shop_here_again", "likelihood_to_recommend",

            "ratings_site_experience_ease_of_finding",
            "ratings_site_experience_design_site",
            "ratings_site_experience_satisfaction_checkout",
            "ratings_site_experience_product_selection",
            "ratings_site_experience_clarity_product_info",
            "ratings_site_experience_charges_stated_clearly",
            "ratings_site_experience_price_relative_other_retailers",
            "ratings_site_experience_shipping_charges",
            "ratings_site_experience_variety_shipping_options",

            "ratings_after_purchase_on_time_delivery",
            "ratings_after_purchase_order_tracking",
            "ratings_after_purchase_product_met_expectations",
            "ratings_after_purchase_customer_support",
            "ratings_after_purchase_product_availability",
            "ratings_after_purchase_returns_process",

            "review_after_purchase_author",
            "review_after_purchase_date",
            "review_after_purchase_content"
        ]

    def get_column_values(self) -> list:
        values = super().get_column_values()
        del values[BizRateReviewItem.TITLE_INDEX]  # remove 'title'
        return values + [
            self["overall_satisfaction"], self["would_shop_here_again"], self["likelihood_to_recommend"],

            self["ratings_site_experience"]["ease_of_finding"],
            self["ratings_site_experience"]["design_site"],
            self["ratings_site_experience"]["satisfaction_checkout"],
            self["ratings_site_experience"]["product_selection"],
            self["ratings_site_experience"]["clarity_product_info"],
            self["ratings_site_experience"]["charges_stated_clearly"],
            self["ratings_site_experience"]["price_relative_other_retailers"],
            self["ratings_site_experience"]["shipping_charges"],
            self["ratings_site_experience"]["variety_shipping_options"],

            self["ratings_after_purchase"]["on_time_delivery"],
            self["ratings_after_purchase"]["order_tracking"],
            self["ratings_after_purchase"]["product_met_expectations"],
            self["ratings_after_purchase"]["customer_support"],
            self["ratings_after_purchase"]["product_availability"],
            self["ratings_after_purchase"]["returns_process"],

            self["review_after_purchase"]["author"],
            self["review_after_purchase"]["date"],
            self["review_after_purchase"]["content"],
        ]

    overall_satisfaction = scrapy.Field()
    would_shop_here_again = scrapy.Field()
    likelihood_to_recommend = scrapy.Field()
    ratings_site_experience = scrapy.Field()
    ratings_after_purchase = scrapy.Field()
    review_after_purchase = scrapy.Field()
