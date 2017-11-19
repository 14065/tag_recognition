import cv2
import numpy as np
from paint import *
from db import *
from tmp_match import *

img = open(image_dir + image_file, 'rb').read()
im = cv2.imread(image_dir + image_file, 1)
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

#image_contours(im)
#db_images_insert(len(todo), len(doing), len(done), img)

find_tag(origin, im)
print("\n")
print(im.shape)

#tmp_match(result, im, tmp)
