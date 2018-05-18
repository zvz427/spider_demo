# -*- coding: utf-8 -*-
'''
多线程爬取斗图啦
生产者和消费者模式
'''
from threading import Thread
from queue import Queue
import time
import requests
from bs4 import BeautifulSoup
from urllib import request
from fake_useragent import FakeUserAgent
starturl = 'https://www.doutula.com/photo/list/'
baseurl = 'https://www.doutula.com/'

class Get_UA(object):
    def get_ua(self):
        headers = {'User_Agent':FakeUserAgent().random}
        return headers

class Producer(Thread):
    def __init__(self,name,q):
        Thread.__init__(self,name=name)
        self.data = q

    def reqnext(self,url):
        req = requests.get(url, headers=Get_UA().get_ua())
        con = BeautifulSoup(req.content, 'html5lib')
        alist = con.find_all('a', class_="col-xs-6 col-sm-3")
        for a in alist:
            imgurl = a.find('img').get('data-original')
            self.data.put(imgurl)
            # print(imgurl, '+++++++++has join the queue!+++++++++++++')

        nextpage = baseurl + con.find('ul', class_="pagination").find('a', rel="next").get('href')
        if nextpage:
            self.reqnext(nextpage)

    def run(self):
        self.reqnext(starturl)
        # for i in range(10):
        #     self.data.put(i)
        #     print('{} has produce {}'.format(self.getName(),i))
        #     time.sleep(1)
        # print('{} has complete'.format(self.getName()))

class Customer(Thread):
    def __init__(self,name,q):
        Thread.__init__(self,name=name)
        self.data = q

    def run(self):
        print(self.data.qsize())
        # while not self.data.empty():
        # while True:
        while self.data.qsize()>0:
            print(self.data.qsize())
            time.sleep(0.05)
            try:
                imgurl = self.data.get()
                if imgurl:
                    path = '/home/zxy/pic_360/doutu/'
                    # request.urlretrieve(imgurl,path+imgurl.split('/')[-1])
                    req = requests.get(imgurl,headers=Get_UA().get_ua())
                    print(imgurl.split('/')[-1])
                    with open(path+imgurl.split('/')[-1],'wb') as f:
                        f.write(req.content)
                        # print(imgurl,'+++++++++has remove from the queue,and save the pic!+++++++++++++')
            except Exception as e:
                print(e,'wrong')

        # for i in range(5):
        #     val = self.data.get()
        #     print('{} has used {}'.format(self.name,val))
        #     time.sleep(0.5)
        # print('{} has used all'.format(self.name))

if __name__ == '__main__':
    q = Queue()

    # p = Producer('pp',q)
    # c = Customer('cc',q)
    # p.start()
    # c.start()
    #
    # p.join()
    # c.join()

    # chuangjian duoxiancheng xiazai baocun
    p = Producer('pp', q)
    p.start()
    time.sleep(5)
    for i in range(20):
        Customer('aa',q).start()
