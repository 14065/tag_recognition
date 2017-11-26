import cv2
import numpy as np
from paint import *
from db import *

def tmp_match(result, image, tmp_gray):
    flag = 0
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc
    w, h = tmp_gray.shape[::-1]
    bottom_right = (top_left[0] + w, top_left[1] + h)

    print('max_val:%s'%max_val)
    print('max_loc: %r' %((max_loc[0],max_loc[1]),))
    midpoint = find_center(top_left[0], w, top_left[1], h)
    print('midpoint: %r' %((midpoint[0],midpoint[1]),))
    if max_val <= 0.6:
        flag = 2
    else:
        img_copy = np.copy(image)
        img_copy = cv2.rectangle(img_copy, top_left, bottom_right, (255,0,0), 1)

        show_img(img_copy)
    return midpoint, flag

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

def point_compare(image, tmp_midpoint, midpoint, image_id, tag_id, flag):
    tolerance_x = (tmp_midpoint[0]-20,tmp_midpoint[0]+20)
    tolerance_y = (tmp_midpoint[1]-20,tmp_midpoint[1]+20)

    if tolerance_x[0] < midpoint[0] < tolerance_x[1] and tolerance_y[0] < midpoint[1] < tolerance_y[1]:
        print('移動していない')
    elif flag == 2:
        print('付箋が外されました')
        """db
        db_flag_update(image_id, tag_id, flag)
        changed_img = encode_img(image)
        db_changed_img_insert(changed_img)
        """
    else:
        flag = 1
        print('移動している')
        """db
        db_flag_update(image_id, tag_id, flag)

        changed_img = cv2.line(image, tmp_midpoint, midpoint, (0,0,0),2)
        cv2.circle(changed_img, tmp_midpoint, 8, (0,0,0), -1)
        changed_img = encode_img(changed_img)
        db_changed_img_insert(changed_img)
        return changed_img
        """
