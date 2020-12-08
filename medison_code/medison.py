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

path = '/home/ubuntu/mini_project/pill.csv'

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

        self.result_url = '/home/ubuntu/mini_project/drug_image_dataset/'
        # 이미지를 저장할 경로 지정



        self.medlist.setText('Found my medison!')
        self.cnt = 0

    def initUI(self):
        self.box1.currentTextChanged.connect(self.BackFind)
        self.box2.currentTextChanged.connect(self.BackFind)
        self.box3.currentTextChanged.connect(self.BackFind)
        self.box4.currentTextChanged.connect(self.BackFind)
        self.medlist2.currentTextChanged.connect(self.selectmed)

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

        #for i in range(len(self.dst)):
        filename = os.path.join(self.result_url, re.split('[<,>,\[,\],/,-,(,),1,2,3,4,5,6,7,8,9,0. :]', self.dstdf['품목명'])[self.cnt] + '.jpg')
        # ~urlretrieve(a,b) : a에 가서 이미지를 b로 저장
        urllib.request.urlretrieve(self.dstdf['큰제품이미지'], filename)
        # re.split('[/,-,(,). :]' : 품목명에 아스코푸정(히벤즈산티페피딘) --> 아스코푸정 이렇게 나오도록 하려고 해준다

    def ImgShow(self):
        urlString = self.dstdf['큰제품이미지'][self.cnt]


        for i in os.listdir(self.result_url):
            if i == (re.split('[<,>,\[,\],/,-,(,),1,2,3,4,5,6,7,8,9,0. :]', self.dstdf['품목명'][self.cnt])[0] + '.jpg'):
                self.Imgurl = os.path.join(self.result_url,i)


        self.Imgurl = urllib.request.urlopen(urlString).read()

        self.qPixmapFileVar = QPixmap()
        self.qPixmapFileVar.loadFromData(self.Imgurl)
        self.qPixmapFileVar = self.qPixmapFileVar.scaledToHeight(140)
        self.medImg.setPixmap(self.qPixmapFileVar)

        self.medinfo.append(re.split('[<,>,\[,\],/,-,(,),1,2,3,4,5,6,7,8,9,0. :]', self.dstdf['품목명'][self.cnt])[0] + '.jpg')
        self.medinfo.append(self.dstdf['분류명'][self.cnt])
        self.medinfo.append(self.dstdf['업소명'][self.cnt])
        self.medinfo.append(self.dstdf['성상'][self.cnt])

    def SaveImg(self):
        self.qPixmapSaveVar = self.medImg.pixmap()
        self.qPixmapSaveVar.save("SavedImage.jpg")

    def NextImg(self):
        self.cnt += 1
        if self.dstdf['큰제품이미지'][self.cnt] is None:
            self.cnt -= 1

        self.ImgShow()

    def UndoImg(self):
        self.cnt -= 1
        if self.dstdf['큰제품이미지'][self.cnt] is None:
            self.cnt += 1

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
        self.ImgSave()


if __name__ == "__main__" :
    # 약 정보가 들어있는 데이터를 데이터 프레임으로 만들기
    df = pd.read_csv(path)

    app = QApplication(sys.argv)
    myMedison = FindMedison()
    myMedison.show()
    app.exec_()
