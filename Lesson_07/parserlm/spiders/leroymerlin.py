import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from Lesson_07.parserlm.items import ParserlmItem


class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response: HtmlResponse, **kwargs):
        next_page = response.xpath(
            '//a[@data-qa-pagination-item="right"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//a[@data-qa='product-image']")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    @staticmethod
    def parse_ads(response: HtmlResponse):
        loader = ItemLoader(item=ParserlmItem(), response=response)
        loader.add_xpath('name', '//h1//text()')
        loader.add_xpath('price', '//span[@slot="price"]//text()')
        loader.add_value('link', response.url)
        loader.add_xpath('photos', '//source[@media=" only screen and (min-width: 1024px)"]//@srcset')
        loader.add_xpath('specs', '//div[@class="def-list__group"]//text()')
        yield loader.load_item()