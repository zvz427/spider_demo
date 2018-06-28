'''
爬取海报链接
请求不到下一页数据   qingqiu budao xiayiye ji tngzhi ,weijiejue
'''
import requests
from urllib import request
from bs4 import BeautifulSoup
import re
import time


starturl = 'https://www.647aa.com/htm/movielist1/'
# /htm/movielist1/2.htm
class Climb_632aa(object):
    def __init__(self):
        self.baseurl = 'https://www.647aa.com'
        self.basepornurl = 'http://666.maomixia666.com:888'

    def work(self,starturl=''):
        obj = self.startrequest(starturl=starturl)
        self.parse(obj)

    def startrequest(self,starturl=''):
        headers = {'User_Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
        try:
            time.sleep(0.5)
            req = requests.get(starturl,timeout=1,headers=headers)
            con = req.content.decode('utf-8')
            obj = BeautifulSoup(con,'html5lib')
        except Exception as e:
            print('starturl wrong', e)
            return None
        else:
            return obj

    def parse(self,obj):
        if obj:
            movielists = obj.find('ul',class_="movieList").find_all('a')
            print(movielists)
            for movie in movielists:
                urltail = movie.attrs['href']
                movieurl = self.baseurl + urltail

                # qingqiu dange dizhi
                try:
                    movieobj = self.startrequest(starturl=movieurl)
                except Exception as e:
                    print('movieurl wrong',e)

                # haibao dizhi
                else:
                    if movieobj:
                        posturl = movieobj.find('div', class_="poster").img.attrs['src']
                        pic_title = movieobj.find('div',class_="poster").img.attrs['title']
                        print(posturl)

                        # yingpian dizhi
                        pornurl_tail = re.findall(r'<script type="text/javascript">generate_down(.*?)</script>', str(movieobj))[0].split('"')[1]
                        pornurl = self.basepornurl + pornurl_tail
                        print(pornurl)

                        self.save_con((posturl, pic_title, pornurl))
            # 1/xunhuan zhixing
            for i in range(7,116):
                print('        start request the next page!')
                print(nexturl)
                nexturl = 'https://www.647aa.com/htm/movielist1/'+str(i)+'.htm'
                print(nexturl)
                self.work(starturl=nexturl)
                print('                                         the'+str(i)+'page has completed')

            #2/qingqiu xiayiye
            # nexturl_tail = obj.find('div', class_="pageList").find('a', text=re.compile('下一页')).attrs['href']
            # nexturl = self.baseurl + nexturl_tail
            # if nexturl:
            #     print('        start request the next page!')
            #     print(nexturl)
            #     self.work(starturl=nexturl)
                # self.work(starturl='https://www.647aa.com/htm/movielist1/3.htm')


    def save_con(self,obj):
        (posturl, pic_title, pornurl) = obj
        # baocun tupian
        # request.urlretrieve(posturl,'/home/zxy/PycharmProjects/pachong/'+posturl.rsplit('/')[-1])
        try:
            time.sleep(0.5)
            req3 = requests.get(posturl,timeout=1)
            con3 = req3.content
        except Exception as e:
            print('post pic wrong',e)
        else:
            with open('/home/zxy/pic_360/little_pic/'+pic_title+'-'+posturl.rsplit('/')[-1],'wb') as f:
                f.write(con3)
                print('the  pic has saved!')
        '''
        jilu chongfu yunxing shi hui chongfu xieru
        '''
        with open('/home/zxy/pic_360/little_pic/video_link.txt','a+') as f:
            f.write(pornurl+'\n')
            print('the pornurl has saved!')

        # paqu shiping
        # try:
        #     req3 = requests.get(pornurl,timeout=1)
        #     con3 = req3.content
        # except Exception as e:
        #     print('pornurl wrong',e)
        # else:
        #     with open('/home/zxy/pic_360/little_pic/'+pornurl.rsplit('/')[-1],'wb') as f:
        #         f.write(con3)
        #         print('the porn has saved!')

if __name__ == '__main__':
    t = Climb_632aa().work(starturl='https://www.647aa.com/htm/movielist1/6.htm')
