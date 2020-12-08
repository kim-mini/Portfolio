import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

from pyqtMedisom import *
import pandas as pd
import os
import numpy as np

import urllib.request
import re
import os
import shutil


#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("medison.ui")[0]

path = './pill.csv'

if os.path.isfile(path):
    pass
else:
    print("Not found '{}'".format(path))


# 화면을 띄우는데 사용되는 Class 선언
class FindMedison(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()
        # 약 정보가 들어있는 데이터를 데이터 프레임으로 만들기
        self.df = pd.read_csv(path)

        self.result_url = './drug_image_dataset/'
        # 이미지를 저장할 경로 지정

        self.medlist.setText('Found my medison!')
        self.Fbtn.setText('찾기')
        self.cnt = 1

    def initUI(self):
        self.box1.currentTextChanged.connect(self.BackFind)
        self.box2.currentTextChanged.connect(self.BackFind)
        self.box3.currentTextChanged.connect(self.BackFind)
        self.box4.currentTextChanged.connect(self.BackFind)
        self.medlist2.currentTextChanged.connect(self.selectmed)

        self.savebnt.clicked.connect(self.SaveImg)
        self.Fbtn.clicked.connect(self.Findbtnpush)
        self.nextbtn.clicked.connect(self.NextImg)
        self.undobtn.clicked.connect(self.UndoImg)

    def BackFind(self):
        if not (self.box1.currentText() == '전체'):
            a = '제형은 ' + self.box1.currentText() + '형 입니다\n'
        if self.box1.currentText() == '전체':
            a = ''

        if not (self.box2.currentText() == '전체'):
            b = '모양은 ' + self.box2.currentText() + '이며\n'
        if self.box2.currentText() == '전체':
            b = ''

        if not (self.box3.currentText() == '전체'):
            c = '색깔은 ' + self.box3.currentText() + '색 입니다\n'
            if self.box3.currentText() == '갈색':
                c = '색깔은 ' + self.box3.currentText() + ' 입니다\n'
            if self.box3.currentText() == '남색':
                c = '색깔은 ' + self.box3.currentText() + ' 입니다\n'
            if self.box3.currentText() == '회색':
                c = '색깔은 ' + self.box3.currentText() + ' 입니다\n'
        if self.box3.currentText() == '전체':
            c = ''

        if not (self.box4.currentText() == '전체'):
            d = self.box4.currentText() + '형 무늬가 있어요\n'
        if self.box4.currentText() == '없음':
            d = ''
        if self.box4.currentText() == '전체':
            d = ''

        MainTXT = b + a + c + d
        self.MainTxt.setText('제 약의 ' + MainTXT)

    def Findbtnpush(self):
        self.dstdf = self.df
        self.medlist.setText('')

        if os.path.exists(self.result_url):  # 해당 디렉토리가 있다면
            shutil.rmtree(self.result_url)  # 디렉토리 지우기

        os.mkdir(self.result_url)  # 새로 디렉토리를 만든다

        if not(self.box2.currentText() == '전체'):
            self.dstdf = self.df.loc[self.df['의약품제형'] == self.box2.currentText()]
        if not (self.box3.currentText() == '전체'):
            self.dstdf = self.dstdf.loc[self.dstdf['색상앞'] == self.box3.currentText()]
        if not (self.box1.currentText() == '전체'):
            self.dstdf = self.dstdf.loc[self.dstdf['제형코드명'] == self.box1.currentText()]
        if not (self.box4.currentText() == ('전체')):
            self.dstdf = self.dstdf.loc[self.dstdf['표기내용앞'] == self.box4.currentText()]

        print(self.box2.currentText(),self.box3.currentText(),self.box1.currentText(),self.box4.currentText())
        self.dstdf.reset_index(drop=True, inplace=True)
        #self.ImgSave()

        print(self.dstdf['큰제품이미지'][self.cnt],type(self.dstdf['큰제품이미지'][self.cnt]))

        self.ImgShow()

        if len(self.dstdf) ==0:
            self.medlist.setText('not found your medison')
        #print(range(len(dstdf)))

        for i in range(len(self.dstdf)):
            medisonName = re.split('[<,>,\[,\],/,-,(,),1,2,3,4,5,6,7,8,9,0. :]', self.dstdf['품목명'][i])[0]

            self.medlist.append(medisonName)
            self.medlist2.addItem(medisonName)

    def ImgSave(self):
        self.qPixmapSaveVar = self.medImg.pixmap()
        self.qPixmapSaveVar.save(self.result_url + '/' + self.FileName)

    def ImgShow(self):
        self.FileName = re.split('[<,>,\[,\],/,-,(,),1,2,3,4,5,6,7,8,9,0. :]', self.dstdf['품목명'][self.cnt])[0] + '.jpg'
        urlString = self.dstdf['큰제품이미지'][self.cnt]

        self.qPixmapFileVar = QPixmap()

        if os.path.exists(self.result_url + '/' + self.FileName):
            self.Imgurl = os.path.join(self.result_url,self.FileName)

            self.qPixmapFileVar.load(self.Imgurl)
        else:
            self.Imgurl = urllib.request.urlopen(urlString).read()
            self.qPixmapFileVar.loadFromData(self.Imgurl)

        self.qPixmapFileVar = self.qPixmapFileVar.scaledToHeight(140)
        self.medImg.setPixmap(self.qPixmapFileVar)

        self.medinfo.append(self.FileName)
        self.medinfo.append(self.dstdf['분류명'][self.cnt])
        self.medinfo.append(self.dstdf['업소명'][self.cnt])
        self.medinfo.append(self.dstdf['성상'][self.cnt])
        if not (os.path.exists(self.result_url+'/'+self.FileName)):
            self.ImgSave()

    def SaveImg(self):
        print('savebtn')
        if not (os.path.exists('./Mymedison')):
            os.mkdir('./Mymedison')
        self.qPixmapSaveVar = self.medImg.pixmap()
        self.qPixmapSaveVar.save(SavePath+'/'+self.FileName)

    def NextImg(self):
        if self.cnt == len(self.dstdf)-1:
            self.cnt = 1
        self.cnt += 1
        self.ImgShow()

    def UndoImg(self):
        self.cnt -= 1

        if self.cnt == -1:
            self.cnt = len(self.dstdf)-1

        self.ImgShow()

    def selectmed(self):
        for i in range(len(self.dstdf)):
            medisonName = re.split('[<,>,\[,\],/,-,(,),1,2,3,4,5,6,7,8,9,0. :]', self.dstdf['품목명'][i])[0]

            if medisonName == self.medlist2.currentText():
                self.cnt = i
                urlString = self.dstdf['큰제품이미지'][i]
                Imgurl = urllib.request.urlopen(urlString).read()
                self.qPixmapFileVar = QPixmap()
                self.qPixmapFileVar.loadFromData(Imgurl)
                self.qPixmapFileVar = self.qPixmapFileVar.scaledToHeight(140)
                self.medImg.setPixmap(self.qPixmapFileVar)



if __name__ == "__main__" :
    # 약 정보가 들어있는 데이터를 데이터 프레임으로 만들기
    df = pd.read_csv(path)

    app = QApplication(sys.argv)
    myMedison = FindMedison()
    myMedison.show()
    app.exec_()
