import cv2 as cv
import numpy as np

imageset = ["test_images/image1.jpg", "test_images/image2.jpg", "test_images/image3.jpg",
            "test_images/image4.jpg", "test_images/image5.jpg", "test_images/image6.jpg",
            "test_images/image7.jpg", "test_images/image8.jpg", "test_images/image9.jpg",
            "test_images/image10.jpg", "test_images/image11.jpg", "test_images/image12.jpg",
            "test_images/image13.jpg", "test_images/image14.jpg", "test_images/image15.jpg",
            "test_images/image16.jpg", "test_images/image17.jpg", "test_images/image18.jpg",
            "test_images/image19.jpg", "test_images/image20.jpg"]

for i in range(0, len(imageset)):   
    img_rgb = cv.imread(imageset[i])
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    template = cv.imread('finderPattern.jpg',0)
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
    threshold = 0.4
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    cv.imwrite('match/res{}.jpg'.format(i),img_rgb)