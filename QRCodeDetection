import cv2

imageset = ["test_images/image1.jpg", "test_images/image2.jpg", "test_images/image3.jpg",
            "test_images/image4.jpg", "test_images/image5.jpg", "test_images/image6.jpg",
            "test_images/image7.jpg", "test_images/image8.jpg", "test_images/image9.jpg",
            "test_images/image10.jpg", "test_images/image11.jpg", "test_images/image12.jpg",
            "test_images/image13.jpg", "test_images/image14.jpg", "test_images/image15.jpg",
            "test_images/image16.jpg", "test_images/image17.jpg", "test_images/image18.jpg",
            "test_images/image19.jpg", "test_images/image20.jpg"]

for num in range(0, len(imageset)):
    image = cv2.imread(imageset[num])
    if (image.shape[1] < 1000):
        scale = 1
    else:
        scale = 0.3
    image = cv2.resize(image, (int(image.shape[1] * scale), int(image.shape[0] * scale)))

    qrCode = cv2.QRCodeDetector()
    points = qrCode.detect(image)
    if (points[0] == False):
        continue
    points = points[1][0]
    for i in range(0, 3):
        cv2.line(image, (int(points[i][0]),int(points[i][1])), (int(points[i+1][0]),int(points[i+1][1])), (0, 255, 0), 3)
        if (i == 2):
            cv2.line(image, (int(points[i+1][0]),int(points[i+1][1])), (int(points[0][0]),int(points[0][1])), (0, 255, 0), 3)
    cv2.imwrite('outputV0/QR{}.jpg'.format(num), image)
