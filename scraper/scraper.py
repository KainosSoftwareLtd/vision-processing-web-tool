"""
 Scrapy experiments to try and pull data from ASOS
"""

import json
import logging
import scrapy

class BlogSpider(scrapy.Spider):
    name = 'asosspider'
    start_urls = ['http://www.asos.com/men/a-to-z-of-brands/cat/?cid=1361']
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    def parse(self, response):
        for url in response.css('div.brand-letter a ::attr(href)').extract():
            yield scrapy.Request(response.urljoin(url), callback=self.parse_fine)


    def parse_fine(self, response):
        # For each product-container in the page, get the title of the product
        for item in response.css('li.product-container'):
            url = item.css('a.product-link ::attr(href)').extract_first()
            yield scrapy.Request(response.urljoin(url), callback=self.parse_fine_fine)
        # Move on to the next page if there is one
        next_page = response.css('li.next > a ::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse_fine)


    def parse_fine_fine(self, response):
        yield {
            'product_code': response.css('div.product-code > span ::text').extract_first(),
            'product_url': response.url,
            'title': response.css('div.product-hero h1 ::text').extract_first(),
            'image_url': self.clean_url(response.css('li.image-thumbnail img ::attr(src)')
                                        .extract_first()),
            'tags': response.css('div.product-description li ::text').extract(),
            'colour': self.get_colour(response.css('li.image-thumbnail img ::attr(src)')
                                      .extract_first())
        }


    def get_colour(self, input):
        # TODO: Get list of colours rather than just first in list
        with open('colours.json') as colours_json:
            colours = json.load(colours_json)
            for colour in colours:
                if colour['name'].lower() in input.lower():
                    return colour['name'].lower()
        return None


    def clean_url(self, input):
        return input.split('?')[0]