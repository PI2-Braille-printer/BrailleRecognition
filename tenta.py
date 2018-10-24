#!/usr/bin/python3
# 2018.01.16 01:11:49 CST
# 2018.01.16 01:55:01 CST
import cv2
import numpy as np
import sys
## (1) read
img = cv2.imread(sys.argv[1])
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

## (2) threshold
th, threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)

cv2.imwrite("kk.jpeg", threshed)
## (3) minAreaRect on the nozeros
pts = cv2.findNonZero(threshed)
ret = cv2.minAreaRect(pts)

(cx,cy), (w,h), ang = ret

if w>h:
    w,h = h,w
    ang += 0 # era 90, mas n quero rotacionar

## (4) Find rotated matrix, do rotation
M = cv2.getRotationMatrix2D((cx,cy), ang, 1.0)
rotated = cv2.warpAffine(threshed, M, (img.shape[1], img.shape[0]))

## (5) find and draw the upper and lower boundary of each lines
hist = cv2.reduce(rotated,1, cv2.REDUCE_AVG).reshape(-1)

th = 2
H,W = img.shape[:2]
uppers = [y for y in range(H-1) if hist[y]<=th and hist[y+1]>th]
lowers = [y for y in range(H-1) if hist[y]>th and hist[y+1]<=th]

rotated = cv2.cvtColor(rotated, cv2.COLOR_GRAY2BGR)

conta = 0

a=[]
b=[]

for y in uppers:
    cv2.line(rotated, (0,y), (W, y), (255,0,0), 1)
    print('comeco', y, W)
    a.append((y, w))
    conta = (conta+1)%3

conta = 0
for y in lowers:
    
    cv2.line(rotated, (0,y), (W, y), (0,255,0), 1)
    print('fim', y, W)
    b.append((y,W))
    conta = (conta+1)%3


zipado = list(zip(a,b))
print(zipado)

for trecho in zipado:
    print(trecho)
    crop_img = rotated[trecho[0][0]+1:trecho[1][0], 0:2*int(trecho[0][1])]
    print(crop_img.shape)
    CORTE = crop_img.shape[1]//26
    print(CORTE)
    cv2.imshow('xd', crop_img)
    cv2.waitKey(0)


cv2.imwrite("result.png", rotated)
