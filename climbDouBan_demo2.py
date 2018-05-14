from urllib import request
import re
import os
from bs4 import BeautifulSoup
import pymysql
import time

num=0

class HttpReqest(object):
    @staticmethod
    def reqestUrl(url):
        req = request.urlopen(url)
        content = req.read()
        return content

class GetPage(object):

    def __init__(self,path='./',baseurl=''):
        self.path = path
        self.url = baseurl
    def startRequest(self,url):

        content = HttpReqest.reqestUrl(url)
        if content:
            content = content.decode('utf-8')
            self.parsePage(content)
            detailurls = self.getDetail(content)
            for detailurl in detailurls:
                info = self.parseDetail(detailurl)
                self.save_detail(info)
                # self.save_mysql(info)

            nexturl = self.nextPage(content)
            if nexturl:
                time.sleep(1)
                self.startRequest(nexturl)

    def saveImg(self,name,url):
        path = os.path.join(self.path,name)
        request.urlretrieve(url,path)

    def parsePage(self,obj):
        if obj:
            divlist = re.findall(r'<div class="item">.*?</div>',obj,re.S)
            if divlist:
                for i in divlist:
                    result = re.search(r'alt="(.*)?" src="(.*?)"',i)
                    if result:
                        name , url = result.groups()
                        tail = url.rsplit('.')
                        # print(tail)
                        name = name + '.' + tail[-1]
                        self.saveImg(name,url)
                        print(name,url)
                        #xia meiye diyizhang
                        # break

    # 解析每个影片的url地址
    def getDetail(self,obj):
        content = BeautifulSoup(obj,'html5lib')

        result = content.find_all('div',class_='item')
        detailurl = []
        for i in result:
            result2 = i.find('a').attrs['href']
            # print(result2)
            detailurl.append(result2)
        # print(detailurl)
        return detailurl

    #解析每个影片的详情页文本
    def parseDetail(self,url):
        content = HttpReqest.reqestUrl(url).decode('utf-8')
        obj = BeautifulSoup(content, 'html5lib')
        result = obj.find('div', class_='indent clearfix')
        result1 = result.find(id="info").text
        info = result1.split('\n')
        info_list = [i.strip() for i in info if i.strip()]
        # print(info_list)
        info_list = [i.split(':') for i in info_list ]
        print(info_list)
        finall_info = {}
        try:
            finall_info = dict(info_list)
            print(finall_info)
        except Exception as e:
            print(e)
            finall_info = {'info':e}
        return finall_info

    # 保存得到详情页的信息
    def save_detail(self,obj):
        global num
        num = num + 1
        f = open(self.path+'/'+str(num)+'info.txt','w')
        f.write(str(obj))
        f.close()

    #保存到mysql
    def save_mysql(self,obj):
        conn = pymysql.connect(
            host="localhost",
            port=3306,
            user="zxy",
            password="zz",
            db="test6",
            charset="utf8"
        )
        cursor = conn.cursor()
        for key,value in obj.items():

            args = [key,value]
            sql = "insert into del(id,name,val) values(0,%s,%s)"
            count = cursor.execute(sql, args)
            conn.commit()
        print(count)

    def nextPage(self,obj):

        if obj:
            next_page = re.search(r'<span class="next">.*?</span>',obj,re.S).group()
            # print(next_page)
            if next_page:
                newurl = re.search(r'href="(.*?)"',next_page).groups()
                # print(newurl)
                next_url = self.url + newurl[0]
                print(next_url)
                return self.url + newurl[0]

if __name__ == '__main__':
    targeturl = 'https://movie.douban.com/top250'
    t1 = GetPage(path='/home/zxy/IMG/pachong',baseurl=targeturl)

    t1.startRequest(targeturl)

