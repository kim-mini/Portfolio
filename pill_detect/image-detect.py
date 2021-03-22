import cv2
import numpy as np
from image_rotation import deskew



img = cv2.imread( './dataset/train/class20_train_1.jpg', cv2.IMREAD_GRAYSCALE )
# 원하는 부분 마스크 영역 생성
b_bg = np.zeros_like(img)
cv2.circle(b_bg, (638,479), 410, (255, 255, 255), -1)
# 필요한 부분만 마스크
img = cv2.bitwise_and( img, img, mask=b_bg )
b_bg_invert = cv2.bitwise_not( b_bg )
# 배경을 흰색으로 만들어 주었다
dst = cv2.add(img, b_bg_invert)
#cv2.imshow( 'image1', dst )

# 화이트 백에 알약만 있는 이미지에서 saliency map을 만든다
saliency = cv2.saliency.StaticSaliencyFineGrained_create()
( success, saliencyMap ) = saliency.computeSaliency( dst )
saliencyMap = ( saliencyMap * 255 ).astype( 'uint8' )

threshMap = cv2.threshold( saliencyMap.astype( 'uint8' ), 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU )[1]

contours, hierachy = cv2.findContours( threshMap, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE )
area, output = 0, contours[0]

for cnt in contours:
    if ( area < cv2.contourArea( cnt )):
        area = cv2.contourArea( cnt )
        output = cnt

epsilon = 0.02 * cv2.arcLength( output, True )
approx = cv2.approxPolyDP( output, epsilon, True )
x, y, w, h = cv2.boundingRect( approx )
rx = x
ry = y
if ( x > 30 ):
    rx = x - 30
if ( y > 100 ):
    ry = y - 100

dst = dst[ ry:y+h+100, rx:x+w+30]
print(dst.shape)
image = deskew(dst)
cv2.imshow( 'image', image )
cv2.waitKey(0)


cv2.destroyAllWindows()