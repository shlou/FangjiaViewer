# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Zone(scrapy.Item):
    section1 = scrapy.Field()
    section2 = scrapy.Field()
    section1UrlIdLj = scrapy.Field()
    section2UrlIdLj = scrapy.Field()


class Community(scrapy.Item):
    name = scrapy.Field()
    type = scrapy.Field()
    saleStatus = scrapy.Field()
    location1 = scrapy.Field()
    location2 = scrapy.Field()
    room = scrapy.Field()
    areaRange = scrapy.Field()
    area1 = scrapy.Field()
    area2 = scrapy.Field()
    tags = scrapy.Field()
    mainAvgPricePerMm = scrapy.Field()
    minTotalPrice = scrapy.Field()
    minTotalPricePerHouse = scrapy.Field()
    urlIdLj = scrapy.Field()
    # details
    estateDeveloper = scrapy.Field()


class House(scrapy.Item):
    room = scrapy.Field()
    area = scrapy.Field()
    orient = scrapy.Field()
    decoration = scrapy.Field()
    elevator = scrapy.Field()
    flood = scrapy.Field()
    totalFlood = scrapy.Field()
    totalPrice = scrapy.Field()
    urlIdLj = scrapy.Field()
    # details
