# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import csv
import logging
from stemming.porter2 import stem
from .items import KBBReviewItem, EdmundsReviewItem, OrbitzReviewItem


class StopwordsRemovalPipeline(object):
    """ Remove stopwords and generate features for review content. """

    stopwords_filename = "stopwords.txt"
    stopwords_fp = None
    stopwords = set()
    tokenization_regex = r"[\s()<>[\]{}|,.:;?!&$'\"]"
    logger = logging.getLogger(__name__)

    def open_spider(self, spider):
        StopwordsRemovalPipeline.__populate_stopwords()

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        text = item["content"]

        # remove comma in numbers
        numbers = re.findall(r"\s(\d+[,\d]*\d+)\s?", text)
        for number in numbers:
            text = text.replace(number, number.replace(",", ""))

        # remove other commas
        text = re.sub(r"['?,\-\\!\"]", " ", text)
        tokens = StopwordsRemovalPipeline.__tokenize(text)
        item["content"] = tokens
        return item

    @staticmethod
    def __populate_stopwords():
        try:
            StopwordsRemovalPipeline.stopwords_fp = open(StopwordsRemovalPipeline.stopwords_filename)
        except OSError as exc:
            StopwordsRemovalPipeline.logger.error("Error: opening stopwords file {} failed. Exception: {}".format(
                StopwordsRemovalPipeline.stopwords_filename, exc))

        for word in StopwordsRemovalPipeline.stopwords_fp:
            StopwordsRemovalPipeline.stopwords.add(word.strip().lower())

        StopwordsRemovalPipeline.stopwords_fp.close()

    @staticmethod
    def __tokenize(text: str) -> list:
        tokens = []
        words = re.split(StopwordsRemovalPipeline.tokenization_regex, text.lower())
        for word in words:
            stripped = word.strip()
            if len(stripped) > 1 and (stripped not in StopwordsRemovalPipeline.stopwords):
                tokens.append(stripped)
        return tokens


class StemmingReviewsPipeline(object):
    """ Stem features. """

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        for i in range(len(item["content"])):
            word = item["content"][i]
            item["content"][i] = stem(word)
        return item


class ExportToCsvPipeline(object):
    """ Export items. """

    def __init__(self):
        self.pos_features_fp = None
        self.neg_features_fp = None
        self.others_fp = None
        self.logger = logging.getLogger(__name__)

    def open_spider(self, spider):
        if getattr(spider, "is_pos_neg_separated", False):
            pos_features_filename = spider.name + "_features_pos.csv"
            neg_features_filename = spider.name + "_features_neg.csv"
            try:
                self.pos_features_fp = open(pos_features_filename, "a")
            except OSError as exc:
                self.logger.error("Error: opening features file {} failed. Exception: {}".format(pos_features_filename, exc))

            try:
                self.neg_features_fp = open(neg_features_filename, "a")
            except OSError as exc:
                self.logger.error("Error: opening features file {} failed. Exception: {}".format(neg_features_filename, exc))
        else:
            features_filename = spider.name + "_features.csv"
            try:
                self.pos_features_fp = open(features_filename, "a")
            except OSError as exc:
                self.logger.error("Error: opening features file {} failed. Exception: {}".format(features_filename, exc))

        others_filename = spider.name + "_others.csv"
        try:
            self.others_fp = open(others_filename, "a")
            others_writer = csv.writer(self.others_fp, delimiter=",", quoting=csv.QUOTE_ALL)

            if spider.name.startswith("kbb"):
                others_writer.writerow(KBBReviewItem.get_column_headers())
            elif spider.name.startswith("edmunds"):
                others_writer.writerow(EdmundsReviewItem.get_column_headers())
            elif spider.name.startswith("orbitz"):
                others_writer.writerow(OrbitzReviewItem.get_column_headers())
        except OSError as exc:
            self.logger.error("Error: opening others file {} failed. Exception: {}".format(others_filename, exc))

    def close_spider(self, spider):
        self.pos_features_fp.close()

        if self.neg_features_fp is not None:
            self.neg_features_fp.close()

        self.others_fp.close()

    def process_item(self, item, spider):
        others_writer = csv.writer(self.others_fp, delimiter=",", quoting=csv.QUOTE_ALL)
        if type(item).__name__ == "KBBReviewItem":
            others_writer.writerow(item.get_column_values())
        elif type(item).__name__ == "EdmundsReviewItem":
            others_writer.writerow(item.get_column_values())
        elif type(item).__name__ == "OrbitzReviewItem":
            others_writer.writerow(item.get_column_values())

        text = ExportToCsvPipeline.__tokens_to_str(item["content"])
        item["content"] = text
        if getattr(spider, "is_pos_neg_separated", False):
            try:
                if item["will_recommend"] == 1:
                    features_writer = csv.writer(self.pos_features_fp, quoting=csv.QUOTE_ALL)
                    features_writer.writerow(item["content"].split(","))
                elif item["will_recommend"] == 0:
                    features_writer = csv.writer(self.neg_features_fp, quoting=csv.QUOTE_ALL)
                    features_writer.writerow(item["content"].split(","))
                else:
                    self.logger.error("Error: value of will_recommend attribute is unknown.")
            except KeyError:
                self.logger.error("Error: item do not have will_recommend attribute.")
        else:
            features_writer = csv.writer(self.pos_features_fp, quoting=csv.QUOTE_ALL)
            features_writer.writerow(item["content"].split(","))
        return item

    @staticmethod
    def __tokens_to_str(tokens: list) -> str:
        s = ""
        if len(tokens) > 0:
            s += tokens[0]
            for i in range(1, len(tokens)):
                s += ", "
                s += tokens[i]
        return s
