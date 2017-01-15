import scrapy
from scrapy_reviews.items import KBBReviewItem


class KBBReviewSpider(scrapy.Spider):
    name = "kbb_reviews"

    def start_requests(self):
        urls = [
            "http://www.kbb.com/lexus/gx/2016/gx-460-consumer_reviews/?vehicleid=412699&intent=buy-new",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, res):
        def extract_with_css(selector, query):
            text = selector.css(query).extract_first()
            return text.strip() if text is not None else None

        def get_title(selector, query):
            raw_title = extract_with_css(selector, query)
            if raw_title is not None:
                return raw_title
            else:
                return ""

        def get_mileage(selector, query):
            raw_mileage = extract_with_css(selector, query)
            if raw_mileage is not None:
                try:
                    return int(raw_mileage.split()[-1].replace(",", ""))
                except:
                    return 0
            else:
                return 0

        def get_ratings(selector, query):
            rating_list = selector.css(query).css("span::text").extract()
            na = "Not Rated"
            overall = 0 if rating_list[0].strip() == na else int(rating_list[0].strip().split("/")[0])
            value = 0 if rating_list[1].strip() == na else int(rating_list[1].strip().split("/")[0])
            reliability = 0 if rating_list[2].strip() == na else int(rating_list[2].strip().split("/")[0])
            quality = 0 if rating_list[3].strip() == na else int(rating_list[3].strip().split("/")[0])
            performance = 0 if rating_list[4].strip() == na else int(rating_list[4].strip().split("/")[0])
            styling = 0 if rating_list[5].strip() == na else int(rating_list[5].strip().split("/")[0])
            comfort = 0 if rating_list[6].strip() == na else int(rating_list[6].split("/")[0])

            return {
                "overall": overall,
                "value": value,
                "reliability": reliability,
                "quality": quality,
                "performance": performance,
                "styling": styling,
                "comfort": comfort
            }

        def get_pros_cons_rc(selector):
            pro = ""
            con = ""
            rc = 0

            for p in selector.css("p"):
                text = extract_with_css(p, "span.helpful-count > strong::text")
                if text is not None:
                    if text.startswith("Pros"):
                        pro = extract_with_css(p, "p::text").replace("\"", "")
                    elif text.startswith("Cons"):
                        con = extract_with_css(p, "p::text").replace("\"", "")
                else:
                    rc = extract_with_css(p, "p::text").split(":")[1].replace("\xa0", "")

            return {
                "pros": pro,
                "cons": con,
                "rc": rc
            }

        def get_content(selector):
            text = extract_with_css(selector, "::text").replace("\"", "")
            if text == "This customer did not provide a text review.":
                text = "NO TEXT REVIEW"
            hidden_text = extract_with_css(selector, "span.hide::text")
            if hidden_text is not None:
                text += hidden_text.replace("\"", "")
            return text

        def get_helpful_count(selector):
            if len(selector) > 0:
                hc = selector.css("strong::text").extract()
                return hc[0].strip() + "/" + hc[1].strip()
            else:
                return "0/0"

        for html_review in res.css("div.review-section"):
            sections = html_review.css("div.section")
            review = KBBReviewItem()
            review["title"] = get_title(sections[0], "h2.mod-title.with-sub::text")
            review["author"] = extract_with_css(sections[0], "p.with-sub > span[itemprop~=author]::text")
            review["date"] = extract_with_css(sections[0], "meta[itemprop~=datePublished]::attr(content)")
            review["owned_mileage"] = get_mileage(sections[0], "p.duration > strong::text")
            ratings = get_ratings(sections[0], "dl > dd")
            review["ratings_overall"] = ratings["overall"]
            review["ratings_value"] = ratings["value"]
            review["ratings_reliability"] = ratings["reliability"]
            review["ratings_quality"] = ratings["quality"]
            review["ratings_performance"] = ratings["performance"]
            review["ratings_styling"] = ratings["styling"]
            review["ratings_comfort"] = ratings["comfort"]
            tmp = get_pros_cons_rc(sections[1])
            review["pros"] = tmp["pros"]
            review["cons"] = tmp["cons"]
            review["recommend_count"] = tmp["rc"]
            review["content"] = get_content(sections[2].css("p.review-text"))
            review["helpful_count"] = get_helpful_count(sections[2].css("p.helpful-count"))
            yield review

        next_page = res.css("a.pagerLink.pager-next::attr(href)").extract_first()
        if next_page is not None:
            next_page = res.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse)
