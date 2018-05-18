import requests
import os
import mimetypes
import time

# fpath = '/home/zxy/PycharmProjects/pachong/IMG_1481.JPG'
apiurl = 'https://api-cn.faceplusplus.com/facepp/v3/detect'

class Facemark(object):
    def __init__(self,apiurl='',path=''):
        self.apiurl = apiurl
        self.path = path

    def getdata(self,fpath):
        self.fname = os.path.basename(fpath)
        ftype = mimetypes.guess_type(fpath)
        file = {'image_file':(self.fname,open(fpath,'rb'),ftype)}
        payload ={
            'api_key':'nWIo-N1vyuyHhxl1LbG2QxXw9Czsge7s',
            'api_secret':'Mje3bB79qdKtAvjBcykyNFrIivpSHKGe',
            'return_attributes':'gender,age'
        }
        return (file,payload)

    def startrequest(self,file,payload):
        try:
            time.sleep(0.5)
            req = requests.post(apiurl,data=payload,files=file,timeout=1)
            jdata = req.json()
        except Exception as e:
            print('failed',e)
            return None
        else:
            print(jdata)
            return jdata

    def savedata(self,jdata):
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
                    face_rectangle = face['face_rectangle']
                    print(gender,age,face_rectangle)
                    info['id'] = self.fname
                    info['gender'] = gender
                    info['age'] = age
                    info['face_rectangle'] = face_rectangle
                    print(info)
                    with open('./face++.txt','a+') as f:
                        f.write(str(info)+'\n')

    def work(self):
        piclist = os.listdir(self.path)
        for pic in piclist:
            print(self.path,pic)
            self.picpath = self.path + pic
            (file, payload) = self.getdata(self.picpath)
            jdata = self.startrequest(file, payload)
            self.savedata(jdata)

if __name__ == '__main__':
    p1 = Facemark(apiurl=apiurl,path='/home/zxy/pic_360/face_test/')
    p1.work()