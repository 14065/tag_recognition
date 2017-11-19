import cv2
import numpy as np
from paint import *
from db import *
"""
img_rgb = cv2.imread(image_dir + image_file, 1)
temp = cv2.imread(image_out_dir + '3.jpg', 0)

img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
img_copy = np.copy(img_rgb)
result = cv2.matchTemplate(img_gray, temp, cv2.TM_CCOEFF_NORMED)
"""

def tmp_match(result, image, tmp_gray):
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc
    w, h = tmp_gray.shape[::-1]
    bottom_right = (top_left[0] + w, top_left[1] + h)
    #print(w, h)
    print('min_val:%s'%min_val)
    print('max_val:%s'%max_val)
    print('min_loc:')
    print(min_loc)
    print('max_loc:')
    print(max_loc)
    midpoint = find_center(top_left[0], w, top_left[1], h)
    print(midpoint)

    img_copy = np.copy(image)
    img_copy = cv2.rectangle(img_copy, top_left, bottom_right, (255,0,0), 1)

    show_img(img_copy)
    #cv2.imwrite(image_out_dir + "tmp.jpg", img)

def multiple_tmp_match(result, image, tmp_gray):
    img_copy = np.copy(image)
    threshold = 0.60
    loc = np.where(result >= threshold)
    if len(loc[0]) == False:
        print("付箋が無いです")

    w, h = tmp_gray.shape[::-1]
    i = 0
    for top_left in zip(*loc[::-1]):
        bottom_right = (top_left[0] + w, top_left[1] + h)

        img_copy = cv2.rectangle(img_copy, top_left, bottom_right, (255,0,0), 1)
        i += 1

    print(i)
    show_img(img_copy)
    #cv2.imwrite(image_out_dir + "tmp_match.jpg", img)

#multiple_tmp_match(result)
#tmp_match(result)
