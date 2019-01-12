# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

from FangjiaViewer.config import LJCONFIG
from FangjiaViewer.items import Community


class LianjiajiuxiaoquSpider(scrapy.Spider):
    name = 'LianjiaJiuxiaoqu'
    allowed_domains = ['lianjia.com']
    root_url = "https://hz.lianjia.com"
    start_urls = ['https://hz.lianjia.com/xiaoqu/']

    def parse(self, response):
        xpath = "/html/body/div[@class='m-filter']/div[@class='position']/dl[2]/dd/div/div[1]/a"
        selections = response.xpath(xpath)
        for selection in selections:
            link = selection.xpath("@href").extract()[0]  # eg: /ershoufang/xihu/
            url = self.root_url + link
            yield Request(url=url, callback=self.process_section1)

    def process_section1(self, response):
        xpath = "/html/body/div[@class='m-filter']/div[@class='position']/dl[2]/dd/div/div[2]/a"
        selections = response.xpath(xpath)
        for selection in selections:
            link = selection.xpath("@href").extract()[0]  # eg: /ershoufang/cuiyuan/
            url = self.root_url + link
            yield Request(url=url, callback=self.process_section2)

    def process_section2(self, response):
        xpath = "/html/body/div[4]/div[@class='leftContent']/div[@class='resultDes clear']/h2[@class='total fl']/span/text()"
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
            response.url + "/pg" + str(pgIdx) + '/' for pgIdx in range(1, int(max_page))
        ]
        for url in urls:
            yield Request(url=url, callback=self.process_community_list)

    def process_community_list(self, response):
        xpath = "/html/body/div[@class='content']/div[@class='leftContent']/ul[@class='listContent']/li[@class='clear xiaoquListItem']"
        community_list = response.xpath(xpath)
        for sel in community_list:
            link = sel.xpath("div[@class='info']/div[@class='title']/a/@href").extract()[0]

            community = Community()
            community['name'] = sel.xpath("div[@class='info']/div[@class='title']/a/text()").extract()[0]
            community['saleStatus'] = "ershou"
            community['location1'] = sel.xpath("div[@class='info']/div[@class='positionInfo']/a[@class='district']/text()").extract()[0]
            community['location2'] = sel.xpath("div[@class='info']/div[@class='positionInfo']/a[@class='bizcircle']/text()").extract()[0]
            community['room'] = ""
            community['areaRange'] = ""
            community['area1'] = ""
            community['area2'] = ""
            community['tags'] = ""
            community['mainAvgPricePerMm'] = sel.xpath("div[@class='xiaoquListItemRight']/div[@class='xiaoquListItemPrice']/div[@class='totalPrice']/span/text()").extract()[0]
            community['urlIdLj'] = link  # eg: https://hz.lianjia.com/xiaoqu/1811043641802/

            yield Request(url=link, callback=self.process_community_details, meta={'item': community})

    def process_community_details(self, response):
        community = response.meta.get('item').copy()
        return community
