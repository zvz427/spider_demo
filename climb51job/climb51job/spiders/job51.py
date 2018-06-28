# -*- coding: utf-8 -*-
'''
1.20180329,解析网页的职能职责时,部分标签下没有p标签导致无法获取内容
'''
import scrapy
from scrapy import Request
from ..items import Climb51JobItem

class Job51Spider(scrapy.Spider):
    name = 'job51'
    # allowed_domains = ['job51.com']
    # start_urls = ['http://job51.com/']

    #请求搜索页第一页的内容,并回调解析主页内容的函数
    def start_requests(self):
        targeturl = 'https://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=010000&' \
              'keyword=python&keywordtype=2&lang=c&stype=2&postchannel=0000&fromType=1&confirmdate=9'
        # url = 'https://search.51job.com/jobsearch/search_result.php'
        yield Request(targeturl,callback=self.parseMain)

    #解析主页的内容,得到每一个工作的详情页的地址列表
    #循环请求每个详情页,回调解析详情页的函数
    #然后获取下一页的页面地址,如果存在的话,回调解析主页面的函数,持续循环
    def parseMain(self, response):
        joblists = response.xpath('//div[@class="el"]/p[@class="t1 "]/span/a')

        print('+++++++++++++++++++++++++++++++++++++++++++',len(joblists))
        for job in joblists:
            joburl = job.xpath('@href').extract()[0]
            joburl = joburl.split('?')[0]
            yield Request(joburl,callback=self.praseChild)

        nexturl = response.xpath('//a[contains(.,"下一页")]').xpath('@href').extract()[0]
        if nexturl:
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++=',nexturl)
            print('++++++++++++++++++++++++++++++++++++++++++++++++++start next page')
            # self.start_requests(targeturl=nexturl)
            # Request(nexturl, callback=self.parseMain)
            yield Request(nexturl, callback=self.parseMain)

            print('++++++++++++++++++++++++++++++++++++++++++++++++++end next page')

    #解析详情页,用item储存解析下的每个字段属性
    def praseChild(self,response):
        # 实例化一个item的对象,解析的每一个详情页的数据为一个实例化对象
        item = Climb51JobItem()

        body = response.xpath('//div[@class="tCompanyPage"]/div[@class="tCompany_center clearfix"]')

        head = body.xpath('//div[@class="tHeader tHjob"]//div[@class="cn"]')
        item['title'] = head.xpath('./h1').xpath('@title').extract()[0]#python讲师
        item['place'] = head.xpath('./span[@class="lname"]').xpath('text()').extract()[0]#工作地点
        item['pay'] = head.xpath('./strong').xpath('text()').extract()[0] #工资
        item['companyname'] = head.xpath('./p[@class="cname"]/a').xpath('@title').extract()[0]#公司名称
        item['companylink'] = head.xpath('./p[@class="cname"]/a').xpath('@href').extract()[0]#公司网址
        companytype = head.xpath('./p[@class="msg ltype"]').xpath('text()').extract()[0]
        item['companytype'] = ''.join(companytype.split())#公司规模

        middle = body.xpath('.//div[@class="tCompany_main"]')
        basereqinfo = middle.xpath('.//div[@class="t1"]/span').xpath('text()').extract()
        item['pub_date'] = basereqinfo[-1]#发布时间
        item['basereqinfo'] = ','.join(basereqinfo)#工作基本要求   无工作经验', '大专', '招1人', '03-28发布'
        welfare = middle.xpath('.//p[@class="t2"]/span').xpath('text()').extract()
        item['welfare'] = ','.join(welfare) #员工福利  五险一金,员工旅游,出国机会,专业培训,定期体检

        dutyreq = middle.xpath('./div[@class="tBorderTop_box"]/div[@class="bmsg job_msg inbox"]/p').xpath('text()').extract()

        # dutyreq = middle.xpath('./div[@class="tBorderTop_box"]/div[@class="bmsg job_msg inbox"]').xpath('text()').extract()标签下没有内容的方式??????????????????????????????/
        item['dutyreq'] = ','.join(dutyreq)  #岗位职责/任职要求
        item['contract'] = middle.xpath('./div[@class="tBorderTop_box"]/div[@class="bmsg inbox"]/p').xpath('text()').extract()[1].split()[0]
        #联系方式
        return item

