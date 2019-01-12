# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class ZoneDao(Base):
    __tablename__ = 'Zone'

    id = Column(Integer, primary_key=True)  # 主键自增
    section1 = Column(String(100))
    section2 = Column(String(100))
    section1UrlIdLj = Column(String(100))
    section2UrlIdLj = Column(String(100))

    def __init__(self, **items):
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])


class CommunityDao(Base):
    __tablename__ = 'Community'

    id = Column(Integer, primary_key=True)  # 主键自增
    name = Column(String(100))
    type = Column(String(100))
    saleStatus = Column(String(100))
    location1 = Column(String(100))
    location2 = Column(String(100))
    room = Column(String(100))
    areaRange = Column(String(100))
    area1 = Column(String(100))
    area2 = Column(String(100))
    tags = Column(String(100))
    mainAvgPricePerMm = Column(String(100))
    minTotalPrice = Column(String(100))
    minTotalPricePerHouse = Column(String(100))
    urlIdLj = Column(String(100))

    # details
    estateDeveloper = Column(String(100))

    # extra info
    effectiveDate = Column(Date)

    def __init__(self, **items):
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])


class HouseDao(Base):
    __tablename__ = 'House'

    id = Column(Integer, primary_key=True)  # 主键自增
    communityId = Column(Integer, ForeignKey('Community.id'))
    community = relationship(CommunityDao)
    room = Column(String(100))
    area = Column(String(100))
    orient = Column(String(100))
    decoration = Column(String(100))
    elevator = Column(String(100))
    flood = Column(String(100))
    totalFlood = Column(String(100))
    totalPrice = Column(String(100))
    urlIdLj = Column(String(100))

    # extra info
    effectiveDate = Column(Date)

    def __init__(self, **items):
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])
