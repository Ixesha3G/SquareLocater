import sys
import math
from turtle import right
import cv2
import numpy as np

imageset = ["output/QR0.jpg", "output/QR1.jpg", "output/QR2.jpg",
            "output/QR3.jpg", "output/QR4.jpg", "output/QR5.jpg",
            "output/QR6.jpg", "output/QR7.jpg", "output/QR8.jpg",
            "output/QR9.jpg", "output/QR10.jpg", "output/QR11.jpg",
            "output/QR12.jpg", "output/QR13.jpg", "output/QR14.jpg",
            "output/QR15.jpg", "output/QR16.jpg", "output/QR17.jpg",
            "output/QR18.jpg", "output/QR19.jpg"]

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

for num in range(0, len(imageset)):
    image = cv2.imread(imageset[num])
    if image is None:
        print ('Error opening image!')
        continue
    src = cv2.cvtColor(image ,cv2.COLOR_BGR2GRAY)
    # image = cv2.resize(image, (int(image.shape[1] * 0.3), int(image.shape[0] * 0.3)))
    # src = cv2.imread(cv2.samples.findFile("test_images/20220514_153418.jpg"), cv2.IMREAD_GRAYSCALE)
    limit_y = image.shape[0] * 0.07
    limit_x = image.shape[1] * 0.07
    # src = cv2.resize(src, (int(src.shape[1] * 0.3), int(src.shape[0] * 0.3)))

    dst = cv2.Canny(src, 70, 210, None, 3)
    # mask = dst != 0
    # dst = src * (mask[:,:,None].astype(src.dtype))
    # cv2.imshow("window_name", dst)
    # cv2.waitKey()

    # Copy edges to the images that will display the results in BGR
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)

    lines = cv2.HoughLines(dst, 1, np.pi / 180, 70, None, 0, 0)

    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)

            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv2.line(cdst, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)

    linesP = cv2.HoughLinesP(dst, 1, np.pi / 180, 17, None, 30, 10)

    if linesP is not None:
        leftLine = ()
        rightLine = ()
        topLine = ()
        botLine = ()
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            if l[0] < limit_x and l[2] < limit_x:
                #leftLine
                cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)
                leftLine = ((l[0], l[1]), (l[2], l[3]))
            if l[0] > cdstP.shape[1]-limit_x and l[2] > cdstP.shape[1]-limit_x:
                #rightLine
                cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,255,0), 3, cv2.LINE_AA)
                rightLine = ((l[0], l[1]), (l[2], l[3]))
            if l[1] < limit_y and l[3] < limit_y:
                #topLine
                cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (255,0,0), 3, cv2.LINE_AA)
                topLine = ((l[0], l[1]), (l[2], l[3]))
            if l[1] > cdstP.shape[0]-limit_y and l[3] > cdstP.shape[0]-limit_y:
                #botLine
                cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (255,0,255), 3, cv2.LINE_AA)
                botLine = ((l[0], l[1]), (l[2], l[3]))
            # cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)

    if (leftLine == () or rightLine == () or topLine == () or botLine == ()):
        continue
    topLeft = np.float32(np.array(line_intersection(leftLine, topLine)))
    topRight = np.float32(np.array(line_intersection(rightLine, topLine)))
    botLeft = np.float32(np.array(line_intersection(botLine, leftLine)))
    botRight = np.float32(np.array(line_intersection(botLine, rightLine)))
    allCord = np.float32(np.vstack((topLeft, topRight, botRight, botLeft)))
    w1 = np.linalg.norm(topLeft - topRight)
    w2 = np.linalg.norm(botLeft - botRight)
    xW = max(w1, w2)
    h1 = np.linalg.norm(topLeft - botLeft)
    h2 = np.linalg.norm(topRight - botRight)
    yH = max(h1, h2)
    # print(allCord)
    # print(xW)
    # print(yH)
    dst = np.float32(np.array([[0,0],[xW-1, 0], [xW-1, yH-1], [0, yH-1]]))
    M = cv2.getPerspectiveTransform(allCord, dst)
    # print(M)
    warpimg = cv2.warpPerspective(image, M, (src.shape[1],src.shape[0]))
    cv2.imwrite('outputV2/QR_PC{}.jpg'.format(num), warpimg)
    # cv2.imshow("Warp", warpimg)
    # cv2.imwrite('outputV2/QR_PC{}.jpg'.format(num), warpimg[0:warpimg.shape[0]-20, 0:warpimg.shape[1]-20])
    # cv2.imshow("Source", src)
    # cv2.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
    # cv2.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)
    # cv2.waitKey()
