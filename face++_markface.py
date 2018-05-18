'''
????????????????????????????????????????/
'''

import requests
import os
import mimetypes
import time

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class Markface(object):
    def __init__(self,pic_path=''):
        self.pic_path = pic_path
        self.save_path = '/home/zxy/pic_360/face_test_save/c6c1.jpg'
        self.Font3 = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-BI.ttf",10)

    def mark(self,rect_box,text):
        img=Image.open(self.pic_path)
        rect_box = rect_box
        text = text
        drawObject=ImageDraw.Draw(img)
        print(rect_box,type(rect_box),type(rect_box[3]),type(rect_box[2]))
        drawObject.rectangle(rect_box,outline="red",fill="green")
        drawObject.text([rect_box[0],rect_box[1]],text,fill="white",font=self.Font3)#写入文字3
        img.save(self.save_path)
        """以下代码用来显示出画的图片"""
        try:
            image=Image.open(self.save_path)
            image.show()#标准版本的show()方法不是很有效率，因为它先将图像保存为一个临时文件，然后使用xv进行显示。如果没有安装xv，该函数甚至不能工作。但是该方法非常便于debug和test。（windows中应该调用默认图片查看器打开）
        except IOError as e:
            print(e)

# fpath = '/home/zxy/PycharmProjects/pachong/IMG_1481.JPG'
apiurl = 'https://api-cn.faceplusplus.com/facepp/v3/detect'

class Facemark(object):
    def __init__(self,apiurl='',path=''):
        self.apiurl = apiurl
        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        print('图片保存路径:',self.path)

    def getdata(self,fpath):
        self.fname = os.path.basename(fpath)
        ftype = mimetypes.guess_type(fpath)
        file = {'image_file':(self.fname,open(fpath,'rb'),ftype)}
        payload ={
            'api_key':'nWIo-N1vyuyHhxl1LbG2QxXw9Czsge7s',
            'api_secret':'Mje3bB79qdKtAvjBcykyNFrIivpSHKGe',
            'return_attributes':'gender,age,beauty,skinstatus'
        }
        return (file,payload)

    def startrequest(self,file,payload):
        proxy = {'http': '200.5.226.118:80'}

        try:
            time.sleep(0.5)
            req = requests.post(apiurl,data=payload,files=file,timeout=1,proxies=proxy)
            jdata = req.json()
        except Exception as e:
            print('failed',e)
            return None
        else:
            print(jdata)
            return jdata

    def savedata(self,jdata,picpath):
        if jdata:
            try:
                faceslist = jdata['faces']
            except Exception as e:
                print('data wrong',e)
            else:
                for face in faceslist:
                    info = {}
                    attributes = face['attributes']
                    gender = attributes['gender']['value']
                    age = attributes['age']['value']
                    beauty = attributes['beauty']
                    skinstatus = attributes['skinstatus']
                    face_rectangle = face['face_rectangle']
                    print(gender,age,face_rectangle)
                    info['id'] = self.fname
                    info['gender'] = gender
                    info['age'] = age
                    info['beauty'] = beauty
                    info['skinstatus'] = skinstatus
                    info['face_rectangle'] = face_rectangle
                    print(info)
                    with open('./face++.txt','a+') as f:
                        f.write(str(info)+'\n')

                    rect_box = (int(face_rectangle['left']),int(face_rectangle['top']),int(face_rectangle['width']),int(face_rectangle['height']))
                    text = {'年龄':age,'sex':gender,'beauty':beauty}
                    Markface(pic_path=picpath).mark(rect_box=rect_box,text=str(text))

    def work(self):
        piclist = os.listdir(self.path)
        for pic in piclist:
            print(self.path,pic)
            self.picpath = self.path + pic
            (file, payload) = self.getdata(self.picpath)
            jdata = self.startrequest(file, payload)
            self.savedata(jdata,self.picpath)

if __name__ == '__main__':
    p1 = Facemark(apiurl=apiurl,path='/home/zxy/pic_360/face_test/')
    p1.work()