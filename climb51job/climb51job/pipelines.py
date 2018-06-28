# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import json

#baocun wei .txt wenjian
class Climb51jobPipeline_txt(object):

    @classmethod
    def from_crawler(cls,crawler):
        return cls(path = crawler.settings.get('FPATH'))

    def __init__(self,path = ''):
        self.fpath = path

    def open_spider(self,spider):
        self.handler = open(self.fpath,'w+')

    def close_spider(self,spider):
        self.handler.close()

    def process_item(self,item,spider):
        self.handler.write(item)


class Climb51JobPipeline_Mysql(object):

    # TABLE = 'job51'


    @classmethod
    def from_crawler(cls,crawler):
        return cls(host = crawler.settings.get('HOST'),
                   port = crawler.settings.get('PORT'),
                   user = crawler.settings.get('USER'),
                   password = crawler.settings.get('PWD'),
                   db = crawler.settings.get('DBNAME'),
                   args = crawler.settings.get('MYSQLFEEDS'),
                   )

    def process_item(self, item, spider):

        conn = pymysql.connect(
            # host="192.168.20.62",
            host="localhost",
            port=3306,
            user="zxy",
            password="zz",
            db="climb163",
            charset="utf8"
        )
        cursor = conn.cursor()

        title = item['title']
        place = item['place']
        pay = item['pay']
        companyname = item['companyname']
        companylink = item['companylink']
        companytype = item['companytype']
        basereqinfo = item['basereqinfo']
        welfare = item['welfare']
        dutyreq = item['dutyreq']
        contract = item['contract']
        pub_date = item['pub_date']


        args = [title,place,pay,companyname,companylink,companytype,basereqinfo,welfare,dutyreq,contract,pub_date]
        # print(args)
        sql = "insert into job51(id,title,place,pay,companyname,companylink,companytype,basereqinfo,welfare,dutyreq,contract,pub_date) values(0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        count = cursor.execute(sql, args)

        conn.commit()
        print(count)
        return item
