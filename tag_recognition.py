import cv2
import numpy as np
from paint import *
from db import *
from tmp_match import *
import time
"""
im = cv2.imread(image_dir + image_file, 1)
img = encode_img(im)
img_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
"""
i = 0
cap = cv2.VideoCapture(0)
while(True):
    if cv2.waitKey(25000) == ord('q'):
        break
    ret, im = cap.read()
    print(i)
    i += 1
    if not ret:
        break
    cv2.imshow('im', im)
    img = encode_img(im)
    img_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    todo_im, doing_im, done_im = each_area_get(im)

    todo = image_pre(todo_im)
    doing = image_pre(doing_im)
    done = image_pre(done_im)
    origin = image_pre(im)

    todo, doing, done = length(todo,doing,done)

    """
    print("number of todo tags: %d" %todo)
    print("number of doing tags: %d" %doing)
    print("number of done tags: %d" %done)
    print("number of origin tags: %d" %len(origin))
    """
    pre_todo, pre_doing, pre_done = get_num_of_previous_tag()

    if todo != pre_todo or doing != pre_doing or done != pre_done:
        db_images_insert(todo, doing, done, img)

        find_tag(origin, im)

        cursor = connect.cursor(dictionary=True, buffered=True)

        sql = "SELECT * FROM tag_info WHERE image_id = %s" %(last_image_id()-1)
        cursor.execute(sql)
        row = cursor.fetchone()
        if row is not None:
            while row is not None:
                tmp = decode_img(row['tag_img'])
                tmp_gray = cv2.cvtColor(tmp, cv2.COLOR_BGR2GRAY)
                #show_img(tmp)

                result = cv2.matchTemplate(img_gray, tmp_gray, cv2.TM_CCOEFF_NORMED)

                midpoint, flag = tmp_match(result, im, tmp_gray)

                tmp_midpoint = (row['midpoint_x'], row['midpoint_y'])

                changed_img, flag = point_compare(im, tmp_midpoint, midpoint, row['image_id'], row['tag_id'], flag)
                calc_time_tag(row['image_id'], row['tag_id'])
                calc_time_tag_stay(row['image_id'], row['tag_id'], tmp_midpoint, row['area'])

                row = cursor.fetchone()

            cv2.imwrite(image_out_dir+str(last_image_id()) + ".jpg", changed_img)
            changed_img = encode_img(changed_img)
            db_changed_img_insert(changed_img)
        else:
            db_changed_img_insert(img)
    else:
        print('変化なし')
cap.release()
cv2.destroyAllWindows()
