import cv2
import numpy as np



img = cv2.imread( './dataset/train/class35_train_1.jpg', cv2.IMREAD_GRAYSCALE )
# 원하는 부분 마스크 영역 생성
b_bg = np.zeros_like(img)
cv2.circle(b_bg, (638,479), 400, (255, 255, 255), -1)
img = cv2.bitwise_and( img, b_bg )
saliency = cv2.saliency.StaticSaliencyFineGrained_create()
( success, saliencyMap ) = saliency.computeSaliency( img )
saliencyMap = ( saliencyMap * 255 ).astype( 'uint8' )
cv2.imshow( 'image1', saliencyMap )

threshMap = cv2.threshold( saliencyMap.astype( 'uint8' ), 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU )[1]
cv2.imshow( 'image2', threshMap )

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

dst = img[ ry:y+h+100, rx:x+w+100]
cv2.imshow( 'image3', img )
cv2.waitKey(0)


cv2.destroyAllWindows()