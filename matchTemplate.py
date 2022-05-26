import cv2
import numpy as np

imageset = ["test_images/image1.jpg", "test_images/image2.jpg", "test_images/image3.jpg",
            "test_images/image4.jpg", "test_images/image5.jpg", "test_images/image6.jpg",
            "test_images/image7.jpg", "test_images/image8.jpg", "test_images/image9.jpg",
            "test_images/image10.jpg", "test_images/image11.jpg", "test_images/image12.jpg",
            "test_images/image13.jpg", "test_images/image14.jpg", "test_images/image15.jpg",
            "test_images/image16.jpg", "test_images/image17.jpg", "test_images/image18.jpg",
            "test_images/image19.jpg", "test_images/image20.jpg"]

for i in range(0, len(imageset)):   
    img_rgb = cv2.imread(imageset[i])
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('finderPattern.jpg',0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.4
    loc = np.where( res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
    cv2.imwrite('matchOutput/res{}.jpg'.format(i),img_rgb)
