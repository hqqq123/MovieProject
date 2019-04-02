# -*- coding: utf-8 -*-
import scrapy

from mySpider.items import MovieItem


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        movies=response.xpath('//div[@class="item"]')
        for movie in movies:
            movieitem=MovieItem()

            movieitem['name']=movie.xpath('.//span[@class="title"]/text()').extract()[0]
            movieitem['info']=movie.xpath('normalize-space(.//p[@class=""]/text())').extract()[0]
            movieitem['area']=movie.xpath('normalize-space(.//p[@class=""]/br)').extract()[0]

            print(movieitem['area'])


