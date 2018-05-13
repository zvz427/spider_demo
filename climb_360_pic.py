'''
使用360的图片接口,采集图片进行人脸识别,
2018/03/24基本优化已完成
'''
import requests
from bs4 import BeautifulSoup
from urllib import request
from fake_useragent import FakeUserAgent
import os
from multiprocessing import Pool

# url = 'http://image.so.com/j?q=%E5%A4%A7%E5%A4%B4%E7%85%A7&src=srp&correct=%E5%A4%A7%E5%A4%B4%E7%85%A7&' \
#       'pn=60&ch=&sn=76&sid=69f43574b2b116960b0c1696e1ec6fa2&ran=0&ras=0&cn=0&gn=0&kn=16'

#360图片的下载接口
baseurl = 'http://image.so.com/j?'

pic_id_list = []

class Get_pic360(object):
    #函数初始化传入参数(下载的接口,搜索的关键词)
    def __init__(self,baseurl='',word='beautiful girl',max_num=4,path=''):
        # 图片保存路径
        self.word = str(word)
        self.path = path + self.word + '/'
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        print('图片保存路径:',self.path)
        self.pic_id_list = [i.rsplit('.')[0] for i in os.listdir(self.path)]
        print(self.pic_id_list)
        self.baseurl = baseurl
        self.num = 0
        self.max_num = max_num
        #请求接口的参数
        self.payload = {
                'q': self.word,
                'src': 'srp',
                'correct': self.word,
                'pn': '60',
                'sn': '0',
                'sid': '69f43574b2b116960b0c1696e1ec6fa2',
                'ran': '0',
                'ras': '0',
                'cn': '0',
                'gn': '0',
                'kn': '16',
                }

    #构造请求头
    def getheaders(self):
        user_agent = FakeUserAgent().random
        user_agent = FakeUserAgent().data['browsers']['chrome'][0]
        headers = {'User_Agent':user_agent}
        return headers

    def reqbasepage(self):
        #请求构造完成后的网页接口
        req = requests.get(self.baseurl, params=self.payload,headers=self.getheaders())
        #将请求下来的数据转化成json格式
        data = req.json()
        print(data)
        # 图片的链接在json中的list后
        lists = data['list']
        list_num = len(lists)
        print(list_num)
        # 把图片的链接地址,id,当前的图片编号拿出
        print('开始请求第' + str(self.num + 1) + '页的图片 ')
        # imgcon = []
        # pool = Pool(20)
        for list in lists:
            imglink = list['img']
            imgid = list['id']
            pic_id_list.append(imgid)
            imgindex = list['index']
            imgcon = self.requestimg(imglink)
            # imgcon.append(pool.apply_async(self.requestimg,(imglink,)))
            self.save(imgcon, imgid, imgindex)

        #请求下一页的图片
        self.num += 1
        if self.num == self.max_num:
            return
        self.payload['sn'] = (self.num+1)*int(self.payload['pn'])
        self.reqbasepage()

    #解析图片的链接地址
    def requestimg(self,imglink):
        try:
            req = requests.get(imglink,timeout=1)
            content = req.content
        except Exception as e:
            print(e,'请求失败,不保存')
            return None
        else:
            return content

    #保存图片
    def save(self,imgcon,imgid,imgindex):
        if imgcon:
            if imgid in self.pic_id_list:
                print(imgid,'图片已存在')
            else:
                # request.urlretrieve()
                with open(self.path+imgid+'.jpg','wb') as f:
                    f.write(imgcon)
                    print('第' + str(imgindex) + '张已保存')

if __name__ == '__main__':
    # 请求5页图片,每页60张
    p1 = Get_pic360(baseurl=baseurl,word='美女',max_num=5,path='/home/zxy/pic_360/')
    p1.reqbasepage()

