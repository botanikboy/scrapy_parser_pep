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
        data = {
            'number': re.search(
                r'\d+',
                response.css('h1.page-title::text').get()).group(),

            'name': re.search(
                r'\– (.+)',
                response.css('h1.page-title::text').get()).group(1),

            'status': response.css('dt:contains("Status") + dd ::text').get(),
        }
        yield PepParseItem(data)
