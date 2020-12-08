import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

from pyqtMedisom import *
import pandas as pd
import os
import numpy as np



#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("medison.ui")[0]

path = '/home/ubuntu/mini_project/pill.csv'

if os.path.isfile(path):
    pass
else:
    print("Not found '{}'".format(path))



#화면을 띄우는데 사용되는 Class 선언
class FindMedison(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.initUI()
        # 약 정보가 들어있는 데이터를 데이터 프레임으로 만들기
        self.df = pd.read_csv(path)

    def initUI(self):
        self.box1.currentTextChanged.connect(self.BackFind)
        self.box2.currentTextChanged.connect(self.BackFind)
        self.box3.currentTextChanged.connect(self.BackFind)
        self.box4.currentTextChanged.connect(self.BackFind)

        self.Fbtn.clicked.connect(self.Findbtnpush)

    def BackFind(self):
        if not(self.box1.currentText() == '전체'):
            a = '제형은 '+self.box1.currentText()+'형 입니다\n'
        if self.box1.currentText() == '전체':
            a = ''

        if not(self.box2.currentText() == '전체'):
            b = '모양은 '+self.box2.currentText()+'이며\n'
        if self.box2.currentText() == '전체':
            b = ''

        if not (self.box3.currentText() == '전체'):
            c = '색깔은 '+ self.box3.currentText() + '색 입니다\n'
            if self.box3.currentText() == '갈색':
                c = '색깔은 ' + self.box3.currentText() + ' 입니다\n'
            if self.box3.currentText() == '남색':
                c = '색깔은 ' + self.box3.currentText() + ' 입니다\n'
            if self.box3.currentText() == '회색':
                c = '색깔은 ' + self.box3.currentText() + ' 입니다\n'
        if self.box3.currentText() == '전체':
            c = ''

        if not (self.box4.currentText() == '전체'):
            d = self.box4.currentText()+'형 무늬가 있어요\n'
        if self.box4.currentText() == '없음':
            d = ''
        if self.box4.currentText() == '전체':
            d = ''

        MainTXT = b+a+c+d
        self.MainTxt.setText('제 약의 '+ MainTXT)


    def Findbtnpush(self):
        dstdf = self.df.loc[self.df['의약품제형'] == self.box2.currentText()]
        dstdf = dstdf.loc[dstdf['색상앞'] == self.box3.currentText()]
        dstdf = dstdf.loc[dstdf['제형코드명'] == self.box1.currentText()]
        dstdf = dstdf.loc[dstdf['표기내용앞'] == self.box4.currentText()]
        print(dstdf.value_counts())

if __name__ == "__main__" :


    app = QApplication(sys.argv)
    myMedison = FindMedison()
    myMedison.show()
    app.exec_()
