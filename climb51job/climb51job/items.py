# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 定义储存的数据的属性字段
class Climb51JobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    place = scrapy.Field()
    pay = scrapy.Field()
    companyname = scrapy.Field()
    companylink = scrapy.Field()
    companytype = scrapy.Field()
    pub_date = scrapy.Field()
    basereqinfo = scrapy.Field()
    welfare = scrapy.Field()
    dutyreq = scrapy.Field()
    contract = scrapy.Field()

