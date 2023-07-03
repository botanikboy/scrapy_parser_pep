import re
import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        for pep_link in response.css('a[href^="pep-"]'):
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        title = response.css('h1.page-title::text').get()
        pattern = r'(?P<number>\d+) \– (?P<name>.+)'
        number, name = re.search(pattern, title).groups()
        data = {
            'number': number,
            'name': name,
            'status': response.css('dt:contains("Status") + dd ::text').get(),
        }
        yield PepParseItem(data)
