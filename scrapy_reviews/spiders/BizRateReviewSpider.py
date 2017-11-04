import datetime
import scrapy
from scrapy_reviews.items import BizRateReviewItem


class BizRateReviewSpider(scrapy.Spider):
    name = "bizrate_overstock"

    def start_requests(self):
        urls = [
            "http://www.bizrate.com/reviews/overstock.com/23819/"
            # "http://www.bizrate.com/reviews/ld-products/27964/"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.logger.info("Parsing page " + response.url)

        selectors = response.xpath("//li[@class='review-item']")

        for selector in selectors:
            link = selector.xpath("ul/div[2]/div/div/li[@class='links']/a/@href").extract_first()
            yield scrapy.Request(url="http://www.bizrate.com" + link.strip(), callback=self.process_details)

        next_urls = response.xpath(
            "//ul[@id='pagination']/li[@class='page current']/following-sibling::li[@class='page ']/a/@href").extract()
        for url in next_urls:
            yield scrapy.Request(url="http://www.bizrate.com" + url.strip(), callback=self.parse)

    def process_details(self, response):
        self.logger.info("Parsing review details: " + response.url)
        review = BizRateReviewItem()
        store_ratings = response.xpath("//*[@id='store_ratings']")

        review["author"] = store_ratings.xpath("div[@class='authorship']/p[@class='author']/text()").extract_first()
        review["review_after_purchase"]["author"] = review["author"]

        rating_scores = store_ratings.xpath("div[3]/div[1]/div/div")
        review["overall_satisfaction"] = self._extract_score(
            rating_scores.xpath("p[@class='rating'][1]/span[1]/text()").extract_first())
        review["would_shop_here_again"] = self._extract_score(
            rating_scores.xpath("p[@class='rating'][2]/span[1]/text()").extract_first())
        review["likelihood_to_recommend"] = self._extract_score(
            rating_scores.xpath("p[@class='rating'][3]/span[1]/text()").extract_first())

        rating_site_items = store_ratings.xpath("div[3]/div[2]/div[1]/div/div[@class='ratings']/span/@title").extract()
        rating_site_scores = [self._extract_rating(s) for s in rating_site_items]
        review["ratings_site_experience"]["ease_of_finding"] = rating_site_scores[0]
        review["ratings_site_experience"]["design_site"] = rating_site_scores[1]
        review["ratings_site_experience"]["satisfaction_checkout"] = rating_site_scores[2]
        review["ratings_site_experience"]["product_selection"] = rating_site_scores[3]
        review["ratings_site_experience"]["clarity_product_info"] = rating_site_scores[4]
        review["ratings_site_experience"]["charges_stated_clearly"] = rating_site_scores[5]
        review["ratings_site_experience"]["price_relative_other_retailers"] = rating_site_scores[6]
        review["ratings_site_experience"]["shipping_charges"] = rating_site_scores[7]
        review["ratings_site_experience"]["variety_shipping_options"] = rating_site_scores[8]

        rating_after_items = store_ratings.xpath("div[3]/div[2]/div[2]/div/div[@class='ratings']/span/@title").extract()
        rating_after_scores = [self._extract_rating(s) for s in rating_after_items]
        review["ratings_after_purchase"]["on_time_delivery"] = rating_after_scores[0]
        review["ratings_after_purchase"]["order_tracking"] = rating_after_scores[1]
        review["ratings_after_purchase"]["product_met_expectations"] = rating_after_scores[2]
        review["ratings_after_purchase"]["customer_support"] = rating_after_scores[3]
        review["ratings_after_purchase"]["product_availability"] = rating_after_scores[4]
        review["ratings_after_purchase"]["returns_process"] = rating_after_scores[5]

        review_site = store_ratings.xpath("div[@*[name()='tal:condition']='posReviewText']")
        if len(review_site) > 0:
            review["date"] = self._reformat_date(review_site.xpath("div/p[1]/text()").extract_first())
            review["content"] = review_site.xpath("div/p[2]/text()").extract_first().strip()

        review_after = store_ratings.xpath("div[@*[name()='tal:condition']='reviewText']")
        if len(review_after) > 0:
            review["review_after_purchase"]["date"] = self._reformat_date(
                review_after.xpath("div/p[1]/text()").extract_first())
            review["review_after_purchase"]["content"] = review_after.xpath("div/p[2]/text()").extract_first().strip()

        return review

    def _extract_score(self, score_str: str) -> int:
        return -1 if score_str.lower() == 'unavailable' else int(score_str)

    def _extract_rating(self, rating_str: str) -> int:
        if rating_str.lower() == 'not rated':
            return -1
        else:
            return int(rating_str.split()[0])

    def _reformat_date(self, date_str: str) -> str:
        # Oct 29, 2017
        return datetime.datetime.strptime(date_str, "%b %d, %Y").date().strftime("%Y%m%d")
