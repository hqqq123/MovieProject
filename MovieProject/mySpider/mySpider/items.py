# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name=scrapy.Field()
    info=scrapy.Field()
    star=scrapy.Field()
    area=scrapy.Field()
    length=scrapy.Field()
    release_time=scrapy.Field()
    url=scrapy.Field()
    logo=scrapy.Field()

