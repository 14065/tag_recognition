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

    #print('max_val:%s'%max_val)
    #print('max_loc: %r' %((max_loc[0],max_loc[1]),))
    midpoint = find_center(top_left[0], w, top_left[1], h)
    #print('midpoint: %r' %((midpoint[0],midpoint[1]),))
    if max_val <= 0.6:
        flag = 2
    else:
        img_copy = np.copy(image)
        img_copy = cv2.rectangle(img_copy, top_left, bottom_right, (255,0,0), 1)

        #show_img(img_copy)
    return midpoint, flag

def point_compare(image, tmp_midpoint, midpoint, image_id, tag_id, flag):
    left, right, top, bottom = tolerance_area(tmp_midpoint)

    if left < midpoint[0] < right and top < midpoint[1] < bottom:
        #print('移動していない')
        db_flag_update(image_id, tag_id, flag)
        return image, flag
    elif flag == 2:
        #print('付箋が外されました')
        db_flag_update(image_id, tag_id, flag)
        return image, flag
    else:
        flag = 1
        #print('移動している')
        db_flag_update(image_id, tag_id, flag)

        changed_img = cv2.line(image, tmp_midpoint, midpoint, (0,0,0),2)
        cv2.circle(changed_img, tmp_midpoint, 8, (0,0,0), -1)
        return changed_img, flag
