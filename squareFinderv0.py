import cv2
image = cv2.imread('test_images/20220514_153418.jpg')
image = cv2.resize(image, (int(image.shape[1] * 0.3), int(image.shape[0] * 0.3)))

qrCode = cv2.QRCodeDetector()
points = qrCode.detect(image)
# print(points)
points = points[1][0]
for i in range(0, 3):
    cv2.line(image, (int(points[i][0]),int(points[i][1])), (int(points[i+1][0]),int(points[i+1][1])), (0, 255, 0), 3)
    if (i == 2):
        cv2.line(image, (int(points[i+1][0]),int(points[i+1][1])), (int(points[0][0]),int(points[0][1])), (0, 255, 0), 3)

cv2.imshow('image', image)
cv2.waitKey()