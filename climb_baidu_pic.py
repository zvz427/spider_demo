from urllib import request
from bs4 import BeautifulSoup
import re
from multiprocessing import Pool
import time

# 分析百度图片的接口api,进行修改爬取图片
def reqesturl(url=''):
    req= request.urlopen(url)
    con = req.read().decode('utf-8')
    return con

def parse(con):
    l = re.findall(r'thumbURL":"(.*?)"',con)
    return l

def save(url,path):
    request.urlretrieve(url,path)

def startget(url=''):
    l =parse(reqesturl(url=url))
    pool = Pool(15)
    for i in l:
        pool.apply_async(save,args=(i,'/home/zxy/mei/'+str(time.time())+'.jpg',))
        # save(i,'/home/zxy/pic/'+str(j)+'.jpg')
        print('保存第'+str(time.time())+'张')
    pool.close()
    pool.join()

if __name__ == '__main__':
    for i in range(1,50):
        num = i
        # url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&' \
        #       'queryWord=%E4%BA%BA%E8%84%B8%E5%9B%BE%E7%89%87&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&' \
        #       'word=%E4%BA%BA%E8%84%B8%E5%9B%BE%E7%89%87&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&fr=&' \
        #       'pn=' + str(30 * num) + '&rn=30&gsm=5a&1521807184174='
        url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&' \
              'queryWord=%E7%BE%8E%E5%A5%B3&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&' \
              'word=%E7%BE%8E%E5%A5%B3&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&cg=girl&' \
              'pn=' + str(30 * num) + '&rn=30&gsm=1e&1521809598631='
        print(url)
        startget(url=url)
        time.sleep(2)
