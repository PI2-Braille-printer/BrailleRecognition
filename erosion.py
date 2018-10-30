import cv2
import numpy as np
import sys

def read_image():
    img = cv2.imread(sys.argv[1])
    return img

def tranform2gray_scale(img):
    gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    cv2.imshow('gray', gray)
    cv2.waitKey()
    return gray

def binarize_image(gray):
    retVal, binarized = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    #binarized = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,2)
    cv2.imshow('binarized',binarized)
    cv2.waitKey()
    return binarized

def perfom_erosion(binarized):
    kernel = np.ones((3,3),np.uint8)
    erosion = cv2.erode(binarized,kernel,iterations=1)
    cv2.imshow('erosion', erosion)
    cv2.waitKey()
    #sys.exit()
    return erosion

def findpointswhereimageisnotblack():
    points = []
    num_colunms = erosion.shape[1]
    for line in range(erosion.shape[0]):
        temp_points= [(line, y) for y in range(num_colunms) if erosion[line][y] > 0]
        if temp_points != []:
            points.append(temp_points)

def reduceimageinx(erosion):
    reduced = cv2.reduce(erosion, 0, cv2.REDUCE_AVG).reshape(-1)
    #cv2.imshow('reduced',reduced)
    #cv2.waitKey()
    return reduced

def findpointboundaries(reduced):
    left_line = [x for x in range(len(reduced)-1) if reduced[x]==0 and reduced[x+1] > 0]
    right_line = [x for x in range(len(reduced)-1) if reduced[x]>0 and reduced[x+1]==0]
    print(left_line)
    print(right_line)
    return (left_line, right_line)

def draw_points_boundaries(image,left_line,right_line):
    for x in left_line:
        cv2.line(image,(x,0),(x,image.shape[0]),(255,0,0),1)

    for x in right_line:
        cv2.line(image,(x,0),(x,image.shape[0]),(255,0,0),1)

    cv2.imshow('finalimage',image)
    cv2.waitKey()
    cv2.imwrite('finalimage.png',image)


def clean_image_points(img):
    kernel = np.ones((3,3),np.uint8)
    opened = cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel)
    #closed = cv2.morphologyEx(opened,cv2.MORPH_CLOSE,kernel)
    cv2.imshow('opened',opened)
    cv2.waitKey()
    return opened
#for line in erosion:
#     print(line)
#     for point in new_points:
#        print(point)
#        if line[point-1] == 0 or line[point+1] == 0:
#            print('entrou no if')
#            cv2.line(erosion,(point-space_threshold,0),(point-space_threshold,reduced.shape[0]),(255,0,0),1)

def get_letters_distance(left_line, right_line):
    positions2crop = []
    avg_pts = avg_point_size(left_line,right_line)
    for i in range(len(left_line)-1):
        i+=1
        distance = left_line[i] - right_line[i-1]
        if distance >= avg_pts:
            positions2crop.append([right_line[i-1],left_line[i]])
    return positions2crop

def crop_letters(img,left_line,right_line):
    '''Se a distancia entre os pontos for maior ou igual a 6
       significa que é outra letra'''
    positions2crop = get_letters_distance(left_line,right_line)
    print(positions2crop)
    begin = 0
    for f,s in positions2crop:
        croped = img[:,begin:f+3]
        cv2.imwrite('letters/croped%d.png'%f,croped)
        begin = s
        last = f
    #last character
    croped = img[:,f:]
    cv2.imwrite('letters/croped%d.png'%(f+1),croped)

def avg_point_size(left_line,right_line):
    points_size = []
    for x in range(len(left_line)-1):
        points_size.append(right_line[x] - left_line[x])

    return int(sum(points_size)/len(points_size))

img = read_image()
gray = tranform2gray_scale(img)
binarized = binarize_image(gray)
#cleaned = binarized
cleaned = clean_image_points(binarized)
reduced = reduceimageinx(cleaned)
left_line, right_line = findpointboundaries(reduced)
print(avg_point_size(left_line,right_line))
#draw_points_boundaries(cleaned,left_line,right_line)
crop_letters(cleaned,left_line,right_line)
#6
##avaliar distancia entre letras
