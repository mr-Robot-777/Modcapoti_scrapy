import scrapy
from scrapy.http import HtmlResponse
from lesson_06.parserjob.items import ParserjobItem


class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python&geo%5Bt%5D%5B0%5D=4']

    def parse(self, response: HtmlResponse, **kwargs):
        next_page = response.xpath('//a[@class="icMQ_ bs_sM _3ze9n _1M2AW f-test-button-dalshe f-test-link-Dalshe"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//span[@class="_1e6dO _1XzYb _2EZcW"]/a/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    @staticmethod
    def vacancy_parse(response: HtmlResponse):
        name = response.xpath('//h1//text()').get()
        salary = response.xpath("//span[@class='_2Wp8I _1e6dO _1XzYb _3Jn4o']//text()").getall()
        link = response.url
        item = ParserjobItem(name=name, salary=salary, link=link)
        yield item
