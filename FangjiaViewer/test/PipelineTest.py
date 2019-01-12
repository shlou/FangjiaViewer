# -*- coding: utf-8 -*-

import unittest

from FangjiaViewer.items import Community
from FangjiaViewer.itemdaos import CommunityDao
from FangjiaViewer.pipelines import FangjiaviewerDbSinkPipeline


class TestFangjiaviewerPipeline(unittest.TestCase):
    pipeline = None

    def setUp(self):
        self.pipeline = FangjiaviewerDbSinkPipeline()

    def testDbInsertData(self):
        item = Community()
        item['urlIdLj'] = 'abc'
        item['name'] = 'x小区'
        item['type'] = 'type'
        item['saleStatus'] = 'saleStatus'
        item['location1'] = 'location1'
        item['location2'] = 'location2'
        item['room'] = 'room'
        item['areaRange'] = 'areaRange'
        item['tags'] = 'tags'
        self.pipeline.process_community_data(item)

    def testQueryData(self):
        community = self.pipeline.session.query(CommunityDao).filter(CommunityDao.type=='type1').first()
        if community:
            print(community.__dict__)
        else:
            print(community)
