# -*- coding: utf-8 -*-
import scrapy


def row_parser():
    pass


class Url58921Spider(scrapy.Spider):
    name = 'url_58921'
    allowed_domains = ['58921.com']
    start_urls = ['http://58921.com/alltime/1996']

    def parse(self, response):
        rows = (response
            .css(".movie_box_office_stats_table")
            .css("tbody")
            .css("tr")
            .extract())

        for ii, row in enumerate(rows):
            yield {"row": row}
