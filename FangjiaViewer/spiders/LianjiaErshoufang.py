# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.http import Request

from FangjiaViewer.config import LJCONFIG
from FangjiaViewer.items import House


class LianjiaershoufangSpider(scrapy.Spider):
    name = "LianjiaErshoufang"
    allowed_domains = ["lianjia.com"]
    root_url = "https://hz.lianjia.com"
    start_urls = ['https://hz.lianjia.com/ershoufang/']

    flood_pattern = re.compile(r"([\u4e00-\u9fff]+楼层)\(共([0-9]*)层\)[0-9]{4}年[\u4e00-\u9fff]+  -  [\u4e00-\u9fff]+")

    def parse(self, response):
        selections = response.xpath(
            "/html/body/div[3]/div[@class='m-filter']/div[@class='position']/dl[2]/dd/div[1]/div/a")
        for selection in selections:
            link = selection.xpath("@href").extract()[0]  # eg: /ershoufang/xihu/
            url = self.root_url + link
            yield Request(url=url, callback=self.process_section1)

    def process_section1(self, response):
        selections = response.xpath(
            "/html/body/div[3]/div[@class='m-filter']/div[@class='position']/dl[2]/dd/div[1]/div[2]/a")
        for selection in selections:
            link = selection.xpath("@href").extract()[0]  # eg: /ershoufang/cuiyuan/
            url = self.root_url + link
            yield Request(url=url, callback=self.process_section2)

    def process_section2(self, response):
        xpath = "/html/body/div[@class='content ']/div[@class='leftContent']/div[@class='resultDes clear']/h2[@class='total fl']/span/text()"
        max_items = response.xpath(xpath).extract()[0]
        max_items = int(max_items)
        xpath = "/html/body/div[@class='content ']/div[@class='leftContent']/ul/li[@class='clear LOGCLICKDATA']"
        item_num_per_page = len(response.xpath(xpath))
        if max_items and item_num_per_page != 0:
            max_page = (max_items + item_num_per_page - 1) / item_num_per_page
        else:
            max_page = LJCONFIG['MAXPAGE']
        # max_page = 2  # TODO: debug
        urls = [
            self.root_url + "/ershoufang/pg" + str(pgIdx) + '/' for pgIdx in range(1, int(max_page))
        ]
        for url in urls:
            yield Request(url=url, callback=self.process_house_list)

    def process_house_list(self, response):
        xpath = "/html/body/div[@class='content ']/div[@class='leftContent']/ul/li[@class='clear LOGCLICKDATA']/div[@class='info clear']"
        house_list = response.xpath(xpath)
        for sel in house_list:
            link = sel.xpath("div[@class='title']/a/@href").extract()[0]  # https://hz.lianjia.com/ershoufang/103102482192.html
            house = House()
            house_info = sel.xpath("div[@class='address']/div[@class='houseInfo']/text()").extract()[0]
            house_infos = house_info.split(" | ")
            house['room'] = house_infos[1]
            house['area'] = house_infos[2]
            house['orient'] = house_infos[3]
            house['decoration'] = house_infos[4]
            house['elevator'] = house_infos[5]
            flood_info = sel.xpath("div[@class='flood']/div[@class='positionInfo']/text()").extract()[0]
            flood_match = self.flood_pattern.match(flood_info)
            house['flood'] = flood_match.group(1)
            house['totalFlood'] = flood_match.group(2)
            price_info = sel.xpath("div[@class='priceInfo']/div[@class='totalPrice']/span/text()").extract()[0]
            house['totalPrice'] = price_info + "0000"  # 万
            house['urlIdLj'] = str.replace(link, self.root_url, "")
            yield Request(url=link, callback=self.process_house_details, meta={'item': house})

    def process_house_details(self, response):
        house = response.meta.get('item').copy()
        return house
