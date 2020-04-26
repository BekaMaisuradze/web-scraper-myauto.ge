from bs4 import BeautifulSoup
import scrapy

class MyautoSpider(scrapy.Spider):
    name = 'myauto'
    allowed_domains = ['myauto.ge']
    start_urls = ['https://www.myauto.ge/en/s/00/0/00/00/00/00/00/cars?stype=0&currency_id=3&det_search=0&ord=7&category_id=m0&keyword=']
    pages_left = 10
    fields = ['Manufacturer', 'Model', 'Category', 'Mileage', 'Gear box type',
            'Doors', 'Wheel', 'Color', 'Interior color', 'VIN', 'Leather interior']
    id = 1

    def parse(self, response):

        detail_page_links = response.css('div.car-name-left a::attr(href)').getall()
        yield from response.follow_all(detail_page_links, self.parse_announcement)

        self.pages_left -= 1
        if self.pages_left > 1:
            next_page = response.css('li.pag-next a::attr(href)').get()
            #yield { 'next_page' : next_page }
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)

    def parse_announcement(self, response):
        res = { 'Id': self.id }
        self.id += 1

        lefts = response.css('table.detail-car-table tr th.th-left')
        for item in lefts:
            soup = BeautifulSoup(item.get(), 'html.parser')
            divs = soup.find_all('div')
            if (len(divs) == 2):
                key = divs[0].string.replace('\xa0', ' ').strip()
                if (key in self.fields):
                    val = divs[1].h2.string if divs[1].h2 else divs[1].string
                    res[key] = ' '.join(val.replace('\xa0', ' ').split()) if val else ''

        rights = response.css('table.detail-car-table tr th.th-right')
        for item in rights:
            soup = BeautifulSoup(item.get(), 'html.parser')
            divs = soup.find_all('div')
            if (len(divs) == 2 and divs[1].i.has_attr('class')):
                key = divs[0].string.replace('\xa0', ' ').strip()
                if (key in self.fields):
                    val = 1 if divs[1].i['class'][1] == 'fa-check' else 0
                    res[key] = val

        res['Customs cleared'] = 1 if len(response.css('.levy-true')) > 0 else 0
        res['Price'] = response.css('span.car-price::text').getall()[-1].strip()

        res['imgs'] = []
        imgs = response.css('div.thumbnail-image img')
        for img in imgs:
            soup = BeautifulSoup(img.get(), 'html.parser')
            res['imgs'].append(soup.img['src'])

        yield res
