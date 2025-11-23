import scrapy
from ..items import QuotesElementsDatabase4Item

class QuoteSpider(scrapy.Spider):
    name = 'quotes-4'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # loop through all quote blocks
        for quote in response.xpath('//div[@class="quote"]'):
            item = QuotesElementsDatabase4Item()
            item['title'] = quote.xpath('.//span[@class="text"]/text()').get()
            item['author'] = quote.xpath('.//small[@class="author"]/text()').get()
            item['tag'] = quote.xpath('.//div[@class="tags"]/meta[@itemprop="keywords"]/@content').get()
            yield item

        # follow pagination
        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
