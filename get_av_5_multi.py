# 基于3优化,多进程
import time
import random
from multiprocessing import Pool

import os
import traceback
import uuid
import pymongo
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

console = logging.StreamHandler()
console.setLevel(logging.INFO)

logger.addHandler(handler)
logger.addHandler(console)


# 最大化窗口
# browser.maximize_window()

publish_num = ""


def set_publish_num(pub=""):
    global publish_num
    if not all([pub]):
        print("publish_num is NOne")
        return None
    publish_num = pub
    return publish_num


# browser = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
def init_web():
    # 定义谷歌驱动的路径
    path = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    
    # 定义不弹出浏览器页面
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    return (path, chrome_options)


def post_to_mongo(record=None):
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['atorrent_net']
    mycol = mydb[publish_num]

    url = mycol.find_one({"url": record.get("url","")})
    if url:
        print(record.get("url",""),"existed")
        print(url)
    else:
        x = mycol.insert_one(record)
        print(x.inserted_id)
        
        
def html_post_to_mongo(href=None):
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['atorrent_net']
    mycol = mydb[publish_num]

    url = mycol.find_one({"url": href})
    if url:
        print(url,"existed")
        return True
    else:
        # x = mycol.insert_one(record)
        return False
    
    
def get_html_info(url):
    current_url, img_url_list, img_path, publisher, publish_num, publish_time, actor, tags, torrent_dict = (
        "", "", "",  "", "", "", "", "", "")
    
    try:
        (path, chrome_options) = init_web()
        browser = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
        # browser = webdriver.Chrome(executable_path=path)
        print("start request url",url)
        browser.get(url)
        time.sleep(30)
        
        current_url = url
       
        html_title = browser.find_element_by_xpath('//*[@id="content"]/main/div/div[1]/div/div/div/div[2]/h1/p').text
        try:
            poster_url = browser.find_element_by_xpath(
                '//*[@id="content"]/main/div/div[1]/div/div/div/div[1]/div/span').get_attribute("data-original")
        except Exception as e:
            poster_url = ""

        try:
            picture_url_1 = browser.find_element_by_xpath(
                '//*[@id="content"]/main/div/div[1]/div/div/div/div[2]/div[2]/div[1]/img').get_attribute("src")
        except Exception as e:
            picture_url_1 = ""
        try:
            picture_url_2 = browser.find_element_by_xpath(
                '//*[@id="content"]/main/div/div[1]/div/div/div/div[2]/div[2]/div[2]/img').get_attribute("src")
        except Exception as e:
            picture_url_2 = ""
        try:
            picture_url_3 = browser.find_element_by_xpath(
                '//*[@id="content"]/main/div/div[1]/div/div/div/div[2]/div[2]/div[3]/img').get_attribute("src")
        except Exception as e:
            picture_url_3 = ""
        try:
            picture_url_4 = browser.find_element_by_xpath(
                '//*[@id="content"]/main/div/div[1]/div/div/div/div[2]/div[2]/div[4]/img').get_attribute("src")
        except Exception as e:
            picture_url_4 = ""
        try:
            publisher = browser.find_element_by_xpath(
                '//*[@id="content"]/main/div/div[1]/div/div/div/div[2]/div[3]/p/a').text
        except Exception as e:
            publisher = ""
        try:
            publish_num = browser.find_element_by_xpath(
                '//*[@id="content"]/main/div/div[1]/div/div/div/div[2]/div[4]/p').text
        except Exception as e:
            publish_num = ""
        try:
            num = publish_num.split(":")[-1].strip()
        except Exception as e:
            num = ""
        try:
            publish_time = browser.find_element_by_xpath(
                '//*[@id="content"]/main/div/div[1]/div/div/div/div[2]/div[5]/p').text
        except Exception as e:
            publish_time = ""
        try:
            actor = browser.find_element_by_xpath(
                '//*[@id="content"]/main/div/div[1]/div/div/div/div[2]/div[7]/p/a').text
        except Exception as e:
            actor = ""
        try:
            tags = browser.find_element_by_xpath('//*[@id="content"]/main/div/div[1]/div/div/div/div[2]/div[8]/p').text
        except Exception as e:
            tags = ""
        try:
            titles_list = []
            sizes_list = []
            torrent_titles = browser.find_elements_by_xpath('//div[@class="torrent-info"]/div/p/a')
    
            for title in torrent_titles:
                title = title.get_attribute("href")
                title = "magnet:?xt=urn:btih:" + title.split("=", 1)[-1]
                titles_list.append(title)
    
            torrent_sizes = browser.find_elements_by_xpath('//div[@class="torrent-info"]/div[2]')
            for size in torrent_sizes:
                size = size.text.replace(".", "_")
                u_id = uuid.uuid1()
                size = str(u_id) + "&" + size
                sizes_list.append(size)
    
            torrent_dict = dict(zip(sizes_list, titles_list))
        except Exception as e:
            torrent_dict = ""

        # print(poster_url,picture_url_1, picture_url_2, picture_url_3, picture_url_4)
        img_url_list = [poster_url,picture_url_1, picture_url_2, picture_url_3, picture_url_4]
        img_path = save_picture(num,img_url_list)
      
    except Exception as e:
        print(traceback.format_exc())
        logger.info(">>---requests html wrong,", url)
    #     重试
    else:
        record = {
            "title": html_title,
            "url": current_url,
            "picture_url": img_url_list,
            "img_path": img_path,
            "publisher": publisher,
            "publish_num": publish_num,
            "publish_time": publish_time,
            "actor": actor,
            "tags": tags,
            "torrent": torrent_dict,
            "create_time": time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        }
        
        post_to_mongo(record=record)
        print("url saved success ",current_url)
        browser.close()
        browser.quit()


def requests_headers():
    head_connection = ['Keep-Alive', 'close']
    head_accept = ['text/html,application/xhtml+xml,*/*']
    head_accept_language = ['zh-CN,fr-FR;q=0.5', 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3']
    head_user_agent = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                       'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                       'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
                       'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']

    # header 为随机产生一套由上边信息的header文件
    header = {
        'Connection': head_connection[random.randrange(0, len(head_connection))],
        'Accept': head_accept[0],
        'Accept-Language': head_accept_language[random.randrange(0, len(head_accept_language))],
        'User-Agent': head_user_agent[random.randrange(0, len(head_user_agent))],
    }
    return header  # 返回值为 header这个字典


def save_picture(num,url_list):
    try:
        if not all(num):
            num = str(time.time())
        path = "atorrent_net/" + publish_num +"/" + num + "/"
        if not os.path.exists(path):
            os.makedirs(path)
        print("saving pic starting...")
        for url in url_list:
            if not all([url]):
                continue
            time.sleep(1)
            try:
                html = requests.get(url=url, headers=requests_headers(),timeout=10)
            except Exception as e:
                print(traceback.format_exc())
                continue
            name = url.split("/")
            name = name[-2] + "&" + name[-1]
            with open(path + name, 'wb') as file:
                file.write(html.content)
            print("saving pic finish", url)
        print("saving pic end")
    except Exception as e:
        print(traceback.format_exc())
        return ""
    else:
        return path


def main(curr_url=""):
    # curr_url = 'https://atorrent.net/studio/s1-no.1-style'
    if not curr_url:
        return None
    pub = set_publish_num(pub=curr_url.split("/")[-1])
    print("publish_num is :",pub)
    if not pub:
        return None
    try:
        (path, chrome_options) = init_web()
        # browser = webdriver.Chrome(executable_path=path, chrome_options=chrome_options)
        browser = webdriver.Chrome(executable_path=path)
        logger.info(">>---starting...")
        for i in range(125, 149):
            url = ''
            try:
                # 打开第一页的页面
                # url = 'https://atorrent.net/studio/e-body/{}/'.format(i)
                url = curr_url + '/{}/'.format(i)
                browser.get(url)
                page_1 = browser.current_window_handle
                time.sleep(10)
                print(">>>>-------------current page:",url)
                # each_page(browser, page_1)
                torrent_titles = browser.find_elements_by_xpath('//div[@class="col-xs-6 col-sm-6 col-md-4 col-lg-3"]/a')
                for title in torrent_titles:
                    href = title.get_attribute("href")
                    title = title.get_attribute("title")
                    # rec = dict()
                    # rec["title"] = title
                    # rec["href"] = href
                    # rec["page"] = url
                    flag = html_post_to_mongo(href=href)
                    if flag:
                        continue
                    get_html_info(href)
                # browser.close()
            except Exception as e:
                logger.info(">>---requests page wrong,",url)
                print(traceback.format_exc())
                continue
            else:
                pass
    except Exception as e:
        print(traceback.format_exc())
    else:
        pass


if __name__ == "__main__":
    url_list = ["https://atorrent.net/studio/k.m.produce"]
    # url_list = ["https://atorrent.net/studio/k.m.produce","https://atorrent.net/studio/oppai","https://atorrent.net/studio/ienergy"]
    p = Pool(3)
    for i in url_list:
        p.apply_async(main, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
# //*[@id="content"]/main/div/div/div/div/div[3]/div/ul/li[13]/button
#

