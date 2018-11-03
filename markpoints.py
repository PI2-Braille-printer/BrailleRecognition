import cv2
import sys
import numpy as np
img = cv2.imread(sys.argv[1])
(h, w) = img.shape[:2]
image_size = h*w
mser = cv2.MSER_create()
mser.setMaxArea(image_size//2)
mser.setMinArea(10)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Converting to GrayScale
_, bw = cv2.threshold(gray, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

regions, rects = mser.detectRegions(bw)
# With the rects you can e.g. crop the letters

for (x, y, w, h) in rects:
    cv2.rectangle(img, (x, y), (x+w, y+h), color=(255, 0, 255), thickness=1)

cv2.imshow('?', img)
cv2.waitKey(0)
