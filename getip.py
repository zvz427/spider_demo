from urllib import request
from bs4 import BeautifulSoup
from fake_useragent import FakeUserAgent
from multiprocessing import Pool
import os
import time

#从66ip网址获取ip,并且对获取的ip进行测试,是否可用

class GetIp(object):
    def __init__(self,url=''):
        self.url = url

    def startrequest(self):

        ua = FakeUserAgent().random
        req = request.urlopen(self.url)
        con = req.read().decode('gb2312')
        obj = BeautifulSoup(con, 'html5lib')
        return obj

    def parse(self,obj):
        iptxt = obj.find('body').text.split('\n\t\n\n\n')[0]
        iplist = iptxt.split('\n\t\t')
        return iplist

    def save(self,content):
        print(content)
        f = open('./ip.txt', 'w+')
        f.write(str(content))
        f.close()
        print('ip地址已保存')

class UsefulId(object):
    # def __init__(self):
    #     # self.iplist = iplist
    #
    #     # print(content,type(content))

    def urltest(self,ip):
        print(os.getpid())
        url = 'http://www.ip138.com'
        proxy = request.ProxyHandler(ip)
        opener = request.build_opener(proxy)
        try:
            req = opener.open(url, timeout=2)
        except Exception as e:
            print(e,'链接失败')
        else:
            print(req.code,type(req.code))
            if req.code == 200:
                print(ip)
                f = open('./usefulip.txt','a+')
                f.write(str(ip['http']))
                f.close()


    def test(self):

        f = open('./ip.txt','r')
        content = eval(f.read())
        pool = Pool(20)
        print('获取的ip个数',len(content))
        for ip in content:
            ip = {'http':ip}
            # self.urltest(ip)

            pool.apply_async(self.urltest,(ip,) )

        pool.close()
        pool.join()


if __name__ == '__main__':
    # url = 'http://www.66ip.cn/mo.php?sxb=&tqsl=1000&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=http%3A%2F%2Fwww.66ip.cn%2F%3Fsxb%3D%26tqsl%3D100%26ports%255B%255D2%3D%26ktip%3D%26sxa%3D%26radio%3Dradio%26submit%3D%25CC%25E1%2B%2B%25C8%25A1'
    # getip = GetIp(url=url)
    # getip.save(getip.parse(getip.startrequest()))

    useip = UsefulId()
    ctime = time.time()
    useip.test()
    print(time.time()-ctime)
