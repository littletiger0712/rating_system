from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from Miapp.items import MiItem


class MiSpider(CrawlSpider):
    name = "mi"


    allowed_domains = ["app.mi.com"]
    download_delay = 2
    start_urls = [
        "http://app.mi.com/topList?page={}".format(i) for i in range(42)
    ]
    rules = [
        Rule(LinkExtractor(allow=("http://app\.mi\.com/details",)), callback='parse_app', follow=True),
    ]

    def parse_app(self, response):

        item = MiItem()
        item['url'] = response.url
        item['name'] = response.xpath("//title").xpath("text()").extract()
        item['review_num'] = response.xpath("//span[@class='app-intro-comment']").xpath("text()").extract()
        item['auth_list'] = response.xpath("//ul[@class='second-ul']").extract()
        item['type'] = response.xpath("//p[@class='special-font action']").xpath("text()").extract_first()
        item['package_name'] = response.xpath("//li[@class='special-li'][1]").xpath("text()").extract()
        item['star_num'] = response.xpath("//div[@class='star1-empty']").extract()
        yield item