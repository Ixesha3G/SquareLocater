import cv2
import numpy as np

imageset = ["test_images/image1.jpg", "test_images/image2.jpg", "test_images/image3.jpg",
            "test_images/image4.jpg", "test_images/image5.jpg", "test_images/image6.jpg",
            "test_images/image7.jpg", "test_images/image8.jpg", "test_images/image9.jpg",
            "test_images/image10.jpg", "test_images/image11.jpg", "test_images/image12.jpg"]

for i in range(0, len(imageset)):

  image = cv2.imread(imageset[i])

  if (image.shape[1] < 1000):
    scale = 1
  else:
    scale = 0.3
  # Resize for better view of the image
  image = cv2.resize(image, (int(image.shape[1] * scale), int(image.shape[0] * scale)))
  image_c = np.copy(image)
  image_c2 = np.copy(image)

  # grayscale
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  # ret, thresh1 = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
  # ret, thresh2 = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
  # ret, thresh3 = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
  # ret, threshNoOTSU1 = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY_INV)
  ret, threshNoOTSU2 = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY_INV)
  # ret, threshNoOTSU3 = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY_INV)

  # Parameters tuning and found that global threshold value 160 
  # Also notice that without OTSU will perform relatively better

  kernel = np.ones((5, 5), np.uint8)
  # dilation = cv2.dilate(thresh2, kernel, iterations=1)
  dilation2 = cv2.dilate(threshNoOTSU2, kernel, iterations=1)

  # Select 5 x 5 Mask for Dilation
  # Perform dilation once to ignore the QR code and only focus on it's square shape

  # contours, hierarchy = cv2.findContours(dilation, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
  contours2, hierarchy = cv2.findContours(dilation2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
  outCnts, hierarchy =  cv2.findContours(dilation2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  # Find Contours were perfomed twice, first will locate all the shapes
  # Second is for locating contours near edge for filtering

  # cv2.drawContours(image_c, contours, -1, (0,255,0), 3)
  # cv2.drawContours(image_c2, contours2, -1, (0,255,0), 3)
  outXmin, outYmin, outW, outH = cv2.boundingRect(outCnts[0])
  
  for cnt in contours2:
    area = cv2.contourArea(cnt)
    xmin, ymin, width, height = cv2.boundingRect(cnt)
    # Obtain the coordinates and width of every contours
    for outcnt in outCnts:
      outXmin, outYmin, outW, outH = cv2.boundingRect(outcnt)
      # Obtain the coordinates and width of contours near edge
    if (xmin == outXmin and ymin == outYmin):
      continue
      # Filter out contours near edge
    extent = area / (width * height)
    # ratio of contour area to bounding rectangle area
    # larger than pi/4 would be more likely as rectangle
    ar = float(width) / height
    # Aspect Ratio: ratio of width to height of bounding rect of the object
    # 1 would be square
    
    
    if (extent > np.pi / 5) and (area > 10000) and (ar > .85 and ar < 1.1):
      # Only area > 4000 is selected
      # Since area less than 4000 is lee likely to contain QR code
      # cv2.rectangle(image, (xmin, ymin), (xmin + width, ymin + height), (0,255,0), 3)
      QR = image[ymin-5:ymin+height+5, xmin-5:xmin+width+5]
      cv2.imwrite('output/QR{}.jpg'.format(i), QR)
        
  # cv2.imshow('thresh 1', thresh1)
  # cv2.imshow('thresh NO OTSU', threshNoOTSU1)
  # cv2.imshow('thresh 2', thresh2)
  # cv2.imshow('thresh NO OTSU 2', threshNoOTSU2)
  # cv2.imshow('thresh 3', thresh3)
  # cv2.imshow('thresh NO OTSU 3', threshNoOTSU3)
  # cv2.imshow('Dilation', dilation)
  # cv2.imshow('Dilation2', dilation2)
  # cv2.imshow('image', image)
  # cv2.imshow('Contours', image_c)
  # cv2.imshow('Contours NO OTSU', image_c2)
  # cv2.waitKey()
  