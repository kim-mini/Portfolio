import cv2
import numpy as np



def image_processing( img ):
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
    if ( y > 50 ):
        ry = y - 50

    after_dst = dst[ ry:y+h+30, rx:x+w+50]
    w_bg = np.ones( shape=(500, 500), dtype=np.int8 )
    # h, w = after_dst.shape
    # print(h, w)
    # after_dst = cv2.add(after_dst, w_bg)

    return after_dst

if __name__=='__main__':
    img1 = cv2.imread( './dataset/train/class35_train_1.jpg', cv2.IMREAD_GRAYSCALE )
    img2 = cv2.imread( './dataset/train/class125_train_1.jpg', cv2.IMREAD_GRAYSCALE )
    img3 = cv2.imread( './dataset/train/class30_train_1.jpg', cv2.IMREAD_GRAYSCALE )
    img4 = cv2.imread( './dataset/train/class25_train_1.jpg', cv2.IMREAD_GRAYSCALE )
    img5 = cv2.imread( './dataset/train/class90_train_1.jpg', cv2.IMREAD_GRAYSCALE )
    img6 = cv2.imread( './dataset/train/class160_train_1.jpg', cv2.IMREAD_GRAYSCALE )

    dst1 = image_processing( img1 )
    dst2 = image_processing(img2)
    dst3 = image_processing(img3)
    dst4 = image_processing(img4)
    dst5 = image_processing(img5)
    dst6 = image_processing(img6)

    cv2.imshow( 'image1', dst1 )
    cv2.imshow('image2', dst2)
    cv2.imshow('image3', dst3)
    cv2.imshow('image4', dst4)
    cv2.imshow('image5', dst5)
    cv2.imshow('image6', dst6)
    cv2.waitKey(0)


    cv2.destroyAllWindows()