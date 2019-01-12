# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

from FangjiaViewer.items import Zone


class LianjiabankuaiSpider(scrapy.Spider):
    name = 'LianjiaBankuai'
    allowed_domains = ['lianjia.com']
    root_url = "https://hz.lianjia.com"
    start_urls = ['https://hz.lianjia.com/ershoufang/']

    def parse(self, response):
        selections = response.xpath(
            "/html/body/div[3]/div[@class='m-filter']/div[@class='position']/dl[2]/dd/div[1]/div/a")
        for selection in selections:
            zone = Zone()
            zone["section1"] = selection.xpath("text()").extract()[0]
            link = selection.xpath("@href").extract()[0]  # eg: /ershoufang/xihu/
            url = self.root_url + link
            zone["section1UrlIdLj"] = link.split("/")
            yield Request(url=url, callback=self.process_section1, meta={'item': zone})

    def process_section1(self, response):
        selections = response.xpath(
            "/html/body/div[3]/div[@class='m-filter']/div[@class='position']/dl[2]/dd/div[1]/div[2]/a")
        for selection in selections:
            zone = response.meta.get('item').copy()
            zone["section2"] = selection.xpath("text()").extract()[0]
            link = selection.xpath("@href").extract()[0]  # eg: /ershoufang/cuiyuan/
            zone["section2UrlIdLj"] = link.split("/")
            yield zone
