from urllib import request
import re
import os
from bs4 import BeautifulSoup

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

            nexturl = self.nextPage(content)
            if nexturl:
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
                        break

    def getDetail(self,obj):
        pass

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

