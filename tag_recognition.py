import cv2
import numpy as np
from paint import *
from db import *
from tmp_match import *

im = cv2.imread(image_dir + image_file, 1)
img = encode_img(im)
img_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
#tmp = cv2.imread(image_out_dir + '2.jpg', 0)
#result = cv2.matchTemplate(img_gray, tmp, cv2.TM_CCOEFF_NORMED)


todo_im, doing_im, done_im = each_area_get(im)

todo = image_pre(todo_im)
print("number of todo tags: %d" %len(todo))

doing = image_pre(doing_im)
print("number of doing tags: %d" %len(doing))

done = image_pre(done_im)
print("number of done tags: %d" %len(done))

origin = image_pre(im)
print("number of origin tags: %d" %len(origin))

#db_images_insert(len(todo), len(doing), len(done), img)

find_tag(origin, im)
print("\n")
print(im.shape)

cursor = connect.cursor(dictionary=True, buffered=True)

sql = "SELECT * FROM tag_info WHERE image_id = %s" %(last_image_id()-1)
cursor.execute(sql)
row = cursor.fetchone()

while row is not None:
    tmp = decode_img(row['tag_img'])
    tmp_gray = cv2.cvtColor(tmp, cv2.COLOR_BGR2GRAY)
    show_img(tmp)

    result = cv2.matchTemplate(img_gray, tmp_gray, cv2.TM_CCOEFF_NORMED)
    print('tag_id:'+str(row['tag_id']))

    #multiple_tmp_match(result, im, tmp_gray)
    midpoint, flag = tmp_match(result, im, tmp_gray)

    tmp_midpoint = (row['midpoint_x'], row['midpoint_y'])
    changed_img = point_compare(im, tmp_midpoint, midpoint, row['image_id'], row['tag_id'], flag)

    print('\n')
    row = cursor.fetchone()
