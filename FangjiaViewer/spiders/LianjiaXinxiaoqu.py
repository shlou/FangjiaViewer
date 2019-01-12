# -*- coding: utf-8 -*-
import re

from scrapy.http import Request
from scrapy.spiders import Spider

from FangjiaViewer.config import LJCONFIG
from FangjiaViewer.items import Community


class LianjiaxinxiaoquSpider(Spider):
    name = "LianjiaXinxiaoqu"
    allowed_domains = ["lianjia.com"]
    root_url = 'https://hz.fang.lianjia.com'
    start_urls = [
        'https://hz.fang.lianjia.com/loupan/'
    ]
    area_range_pattern = re.compile(r"建面 ([1-9][0-9]*)-([1-9][0-9]*)㎡")
    price_pattern = re.compile(r"总价([1-9][0-9]*)万/套起")

    def parse(self, response):
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """
        max_items = response.xpath('/html/body/div[5]/@data-total-count').extract()[0]
        max_items = int(max_items)
        xpath = "/html/body/div[@class='resblock-list-container clearfix']/ul[@class='resblock-list-wrapper']/li[@class='resblock-list post_ulog_exposure_scroll has-results']"
        item_num_per_page = len(response.xpath(xpath))
        if max_items and item_num_per_page != 0:
            max_page = (max_items + item_num_per_page - 1) / item_num_per_page
        else:
            max_page = LJCONFIG['MAXPAGE']
        # max_page = 2  # TODO: debug
        urls = [
            'https://hz.fang.lianjia.com/loupan/pg' + str(pgIdx) + '/' for pgIdx in range(1, int(max_page))
        ]
        for url in urls:
            yield Request(url=url, callback=self.process_community_list)

    def process_community_list(self, response):
        xpath = "/html/body/div[@class='resblock-list-container clearfix']/ul[@class='resblock-list-wrapper']/li[@class='resblock-list post_ulog_exposure_scroll has-results']/div[@class='resblock-desc-wrapper']"
        community_list = response.xpath(xpath)
        for sel in community_list:
            link = sel.xpath("div[@class='resblock-name']/a[@class='name ']/@href").extract()[0]
            community = Community()
            community['name'] = sel.xpath("div[@class='resblock-name']/a[@class='name ']/text()").extract()[0]
            community['type'] = sel.xpath('div[1]/span[1]/text()').extract()[0]
            community['saleStatus'] = sel.xpath('div[1]/span[2]/text()').extract()[0]
            community['location1'] = '|'.join(sel.xpath('div[2]/span/text()').extract())
            community['location2'] = sel.xpath('div[2]/a/text()').extract()[0]
            community['room'] = '|'.join(sel.xpath('a/span/text()').extract())
            area_range = sel.xpath('div[3]/span/text()').extract()[0]
            community['areaRange'] = area_range
            match_string = self.area_range_pattern.match(area_range)
            community['area1'] = match_string.group(1)
            community['area2'] = match_string.group(2)
            community['tags'] = '|'.join(sel.xpath('div[5]/span/text()').extract())
            community['mainAvgPricePerMm'] = sel.xpath('div[6]/div[1]/span/text()').extract()[0]
            community['minTotalPrice'] = sel.xpath('div[6]/div[2]/text()').extract()[0]
            total_price = self.price_pattern.match(community['minTotalPrice'])
            community['minTotalPricePerHouse'] = total_price.group(1) + "0000"  # 万/套
            community['urlIdLj'] = link  # eg: /loupan/p_zcxgafsaj/
            url = self.root_url + link + "xiangqing/"
            yield Request(url=url, callback=self.process_community_details, meta={"item": community})

    def process_community_details(self, response):
        selection = response.xpath("/html/body/div[@class='add-panel clear']/div[@class='big-left fl']")
        community_detail = response.meta.get("item")
        community_detail['estateDeveloper'] = \
            selection.xpath("ul[@class='x-box'][1]/li[@class='all-row'][3]/span[@class='label-val']/text()").extract()[
                0]
        return community_detail
