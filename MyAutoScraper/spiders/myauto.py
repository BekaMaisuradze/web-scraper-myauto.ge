from bs4 import BeautifulSoup
import scrapy

class MyautoSpider(scrapy.Spider):
    name = 'myauto'
    allowed_domains = ['myauto.ge']
    start_urls = ['https://www.myauto.ge/en/s/00/0/00/00/00/00/00/cars?stype=0&currency_id=3&det_search=0&ord=7&category_id=m0&keyword=']
    pages_left = 1

    def parse(self, response):

        detail_page_links = response.css('div.car-name-left a::attr(href)').getall()
        yield from response.follow_all(detail_page_links, self.parse_author)

        self.pages_left -= 1
        if self.pages_left > 1:
            next_page = response.css('li.pag-next a::attr(href)').get()
            yield { 'next_page' : next_page }
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)

    def parse_author(self, response):
        yield {'len': len(response.text) }
