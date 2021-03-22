import os
import cv2

# 원본파일이 있는 경로
path = "../../pill-dataset/test"
listTmp =os.listdir(path)
# 저장할 경로
Savepath = "../../pill-dataset/test2"
# 파일이름+숫자.JPG
num = 0
save_name = f'pill_test_{num}.JPG'

for filename in listTmp:
    imgpath = path + "/" + filename

    img = cv2.imread(imgpath, cv2.IMREAD_COLOR )
    if filename.endswith('JPG'):
        dst = cv2.resize(img, dsize=(640, 480), interpolation=cv2.INTER_AREA)
        Savefile= os.path.join(Savepath,save_name)
        cv2.imwrite( Savefile, dst )
        #print(Savefile)
        num+=1
        save_name = f'pill_test_{num}.JPG'