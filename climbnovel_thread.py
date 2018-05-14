from urllib import request
from bs4 import BeautifulSoup
from threading import Thread
import re
import time
import random
import os
from multiprocessing import Pool,Process

class GetPage(object):
    def __init__(self,baseurl=''):
        self.baseurl = baseurl

    def startreq(self,requrl):
        req = request.urlopen(requrl)
        content = req.read().decode('utf-8')
        con = BeautifulSoup(content, 'html5lib')
        return con

    def parse(self,url):
        con = self.startreq(url)
        bookurllist_tail = con.find('div',class_="books-list").find_all('a')
        # 每一页的25本书的链接

        pool = Pool(20)

        for bookurl_tail in bookurllist_tail:
            bookurl = self.baseurl + bookurl_tail.attrs['href']
            print(bookurl)
            siglebookurl = self.bookurldetail(bookurl)
            print(siglebookurl)

            t = ClimbBook(baseurl=self.baseurl).startrequest
            pool.apply_async(t,(siglebookurl,))
        pool.close()
        pool.join()

            # ClimbBook(baseurl=self.baseurl).startrequest(starturl=siglebookurl)

        if self.getnextpage(con):
            newurl = self.getnextpage(con)
            self.parse(newurl)

    def getnextpage(self,obj):
        nextpageurl_tail = obj.find('a',text=re.compile('下一页')).attrs['href']
        nextpageurl = self.baseurl + nextpageurl_tail
        return nextpageurl

    def bookurldetail(self,bookurl):
        req = request.urlopen(bookurl)
        content = req.read().decode('utf-8')
        con = BeautifulSoup(content, 'html5lib')
        detailurl_tail = con.find('a',text=re.compile('开始阅读')).attrs['href']
        detailurl = baseurl + detailurl_tail
        return detailurl

class ClimbBook(object):
    def __init__(self,baseurl=''):
        self.baseurl = baseurl

    def startrequest(self,starturl):
        try:
            req = request.urlopen(starturl)
            content = req.read().decode('utf-8')
            temp = self.parse(content)
            if not temp:
                print('书已存在')
                return
            else:
                (bookname, title, parge, nexturl) = temp
        except Exception as e:
            print(e)
            print('免费章节已爬取完')
        else:
            self.save(bookname,title, parge)
            '''
            if nexturl:
                # time.sleep(random.randint(1,5))
                self.startrequest(nexturl)
            '''
    def parse(self,obj):
        content = BeautifulSoup(obj,'html5lib')
        bookname = content.find('a', text=re.compile("首页")).find_next('a').text

        path = '/home/zxy/novel/new2/'
        l = os.listdir(path)
        if bookname + '.txt' in l:
            return False

        title = content.find('li',class_="current").text.strip()
        parge = content.find('div',class_="inner-text").text
        nexturl_detail = content.find('li',class_="current").find_next('li').find('a',href=re.compile("html")).attrs['href']
        nexturl = self.baseurl + nexturl_detail
        print(title, parge[:100], nexturl)


        return (bookname,title,parge,nexturl)

    def save(self,bookname,title, parge):

        path = '/home/zxy/novel/new2/'
        if not os.path.exists(path):
            os.makedirs(path)
        print(path+bookname+'.txt')
        f=open(path+bookname+'.txt','a+')
        f.write(title)
        f.write(parge+'\n')
        f.close()

        # f = open('/home/zxy/novel/'+title+'.txt','w')
        # f.write(parge)
        # f.close()
        # print(title,'已保存')

if __name__ == '__main__':
    # 书籍的基本链接
    baseurl = 'http://www.zhuishushenqi.com'
    # 追书神器的书籍开始链接
    # starturl = 'http://www.zhuishushenqi.com/book/50874f79f98e8f7446000017/1.html'
    # climb = ClimbBook(baseurl=baseurl).startrequest(starturl=starturl)
    # climb.startrequest(starturl=starturl)

    # url = 'http://www.zhuishushenqi.com/category?gender=male'
    url = 'http://www.zhuishushenqi.com/category?gender=male'
    url2 = 'http://www.zhuishushenqi.com/category?gender=female'
    p = GetPage(baseurl=baseurl)


    # p1 = p.parse(url)
    # 多线程下载实现???????????????????????------>>>>多线程使用生产者和消费者模式,使用queue队列来解决
    # t1 = Thread(target=p.parse,args=(url,))
    # t2 = Thread(target=p.parse,args=(url2,))
    #
    # t1.start()
    # t2.start()
    #
    # t1.join()
    # t2.join()

    #多进程实现
    t1 = Process(target=p.parse,args=(url,))
    t2 = Process(target=p.parse,args=(url2,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    #进程池????????????????????????????????????
    # outpool = Pool(2)
    # for i in [url,url2]:
    #     print(i)
    #     outpool.apply_async(p.parse,(i,))
    # outpool.close()
    # outpool.join()
