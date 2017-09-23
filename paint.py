import cv2
import numpy as np

image_dir = 'images/'
image_file = 'image3.JPG'

def each_area_get(image):
    height, width = image.shape[:2]
    todo_width = width // 3
    doing_width = 2 * width // 3

    todo_area = image[0:height, 0:todo_width]
    cv2.imwrite("output/todo_area.jpg", todo_area)

    doing_area = image[0:height, todo_width:doing_width]
    cv2.imwrite("output/doing_area.jpg", doing_area)

    done_area = image[0:height, doing_width:width]
    cv2.imwrite("output/done_area.jpg", done_area)

def image_pre(im):
    im_blur = cv2.GaussianBlur(im, (25,25), 0)
    cv2.imwrite("output/im_blur.jpg", im_blur)
    im_th = (np.abs(im_blur[:,:,2] - im_blur[:,:,1]) + np.abs(im_blur[:,:,2] - im_blur[:,:,0]))
    return im_th

def getRectByPoints(points):
    # prepare simple array
    points = list(map(lambda x: x[0], points))

    points = sorted(points, key=lambda x:x[1])
    top_points = sorted(points[:2], key=lambda x:x[0])
    bottom_points = sorted(points[2:4], key=lambda x:x[0])
    points = top_points + bottom_points

    left = min(points[0][0], points[2][0])
    right = max(points[1][0], points[3][0])
    top = min(points[0][1], points[1][1])
    bottom = max(points[2][1], points[3][1])
    return (top, bottom, left, right)

def getPartImageByRect(rect):
    img = cv2.imread(image_dir + image_file, 1)
    return img[rect[0]:rect[1], rect[2]:rect[3]]

def threshold(im_th):
    ret2, th = cv2.threshold(im_th, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return ret2, th

def threshold1(im_th):
    ret1, th1 = cv2.threshold(im_th, 127,255, cv2.THRESH_BINARY)
    return ret1, th1

def threshold2(im_th):
    th2 = cv2.adaptiveThreshold(im_th, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11,3)
    return th2

def contour(im, contours):
    area = im.shape[0] * im.shape[1] / 100
    contours_large = list(filter(lambda c:cv2.contourArea(c) > area, contours))
