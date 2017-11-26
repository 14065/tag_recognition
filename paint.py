import cv2
import numpy as np
from db import *
import os
#import time

image_dir = 'images/pbg/'
image_file = 'WIN_20171026_18_37_42_Pro.jpg'
image_out_dir = 'output/'

def each_area_get(image):
    height, width = image.shape[:2]
    todo_width = width // 3
    doing_width = 2 * width // 3

    todo_im = image[0:height, 0:todo_width]
    #cv2.imwrite(image_out_dir +  "todo_im.jpg", todo_im)

    doing_im = image[0:height, todo_width:doing_width]
    #cv2.imwrite(image_out_dir +  "doing_im.jpg", doing_im)

    done_im = image[0:height, doing_width:width]
    #cv2.imwrite(image_out_dir +  "done_im.jpg", done_im)

    return todo_im, doing_im, done_im

def image_pre(image):
    image = cv2.fastNlMeansDenoisingColored(image,None,10,10,7,21)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)
    h = hsv[:, :, 0]
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]

    mask = np.zeros(h.shape, dtype=np.uint8)
    mask[(h > 0) & (s > 65) & (v > 60)] = 255

    img, contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    area = image.shape[0] * image.shape[1] / 1000
    contours_large = list(filter(lambda c:cv2.contourArea(c) > area, contours))

    return contours_large

"""使わない？
def image_contours(image):
    area_contours_large = image_pre(image)

    img_copy = np.copy(image)
    img_contours = cv2.drawContours(img_copy, area_contours_large, -1, (0,0,0), 2)
    #show_img(img_contours)
    #cv2.imwrite(image_out_dir +  "image-contours.jpg", img_contours)

def threshold(img_th):
    ret2, th = cv2.threshold(img_th, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    cv2.imwrite(image_out_dir +  "image-thresh.jpg", th)

    return ret2, th

def threshold1(img_th):
    ret1, th1 = cv2.threshold(img_th, 127,255, cv2.THRESH_BINARY)
    cv2.imwrite(image_out_dir +  "image-thresh.jpg", th1)

    return ret1, th1

def threshold2(img_th):
    th2 = cv2.adaptiveThreshold(img_th, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11,3)
    cv2.imwrite(image_out_dir +  "image-thresh.jpg", th2)

    return th2
"""

def find_center(x, w, y, h):
    midpoint_x = x + w // 2
    midpoint_y = y + h // 2
    midpoint =  (midpoint_x, midpoint_y)
    return midpoint

def find_tag(contours_large, image):
    max_id = last_image_id()
    TARGET_DIR = image_out_dir + str(max_id) + '/'

    if not os.path.isdir(TARGET_DIR):
        os.makedirs(TARGET_DIR)

    im_copy = np.copy(image)
    #cv2.imwrite(TARGET_DIR + 'origin.jpg', im_copy)

    if(len(contours_large) > 0):
        for i, cnt in enumerate(contours_large):
            x, y, w, h = cv2.boundingRect(cnt)
            bounding_img = cv2.rectangle(im_copy, (x, y), (x + w, y + h), (255, 0, 255), 1)
            #time.sleep(5)

            midpoint = find_center(x, w, y, h)

            print(i)
            print('loc: %r' %((x,y),))
            print('w, h: %r' %((w,h),))
            print('midpoint: %r' %((midpoint[0], midpoint[1]),))

            bounding_img = cv2.circle(bounding_img, midpoint, 3, (0,0,0), -1)

            """db
            img = image[y:y+h, x:x+w]
            img_str = encode_img(img)

            cv2.imwrite(TARGET_DIR+ str(i+1) + ".jpg", img)

            db_tag_insert(i+1, midpoint[0], midpoint[1], img_str)

        cv2.imwrite(TARGET_DIR + "image-bounding.jpg", bounding_img)
"""
def show_img(image):
    cv2.imshow("image",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def decode_img(image):
    nparr = np.fromstring(image, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def encode_img(image):
    ret, image = cv2.imencode('.jpg', image)
    if ret:
        data = np.array(image)
        return data.tostring()
