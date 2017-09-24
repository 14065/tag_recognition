import cv2
import numpy as np
from paint import *
#from sklearn.cluster import KMeans
#KMeans

im = cv2.imread(image_dir + image_file, 1)

todo_im, doing_im, done_im = each_area_get(im)

#写真にブラーをかけ,色の平均を取ってグレースケールに変換
im_th = image_pre(im)
todo_im_th = image_pre(todo_im)
doing_im_th = image_pre(doing_im)
done_im_th = image_pre(done_im)

#todo area
todo_ret2, todo_th = threshold(todo_im_th)
todo_img, todo_contours, _ = cv2.findContours(todo_th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
todo_contours_large = contour(todo_th, todo_contours)
print ("number of tags todo_area: %d" %len(todo_contours_large))

im_copy = np.copy(todo_im)
im_contours = cv2.drawContours(im_copy, todo_contours_large, -1, (0,0,0),2)
show_img(im_contours)

#doing area
doing_ret2, doing_th = threshold(doing_im_th)
doing_img, doing_contours, _ = cv2.findContours(doing_th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
doing_contours_large = contour(doing_th, doing_contours)
print ("number of tags doing_area: %d" %len(doing_contours_large))

im_copy = np.copy(doing_im)
im_contours = cv2.drawContours(im_copy, doing_contours_large, -1, (0,0,0),2)
show_img(im_contours)

#done area
done_ret2, done_th = threshold(done_im_th)
done_img, done_contours, _ = cv2.findContours(done_th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
done_contours_large = contour(done_th, done_contours)
print ("number of tags done_area: %d" %len(done_contours_large))

im_copy = np.copy(done_im)
im_contours = cv2.drawContours(im_copy, done_contours_large, -1, (0,0,0),2)
show_img(im_contours)

#original image
ret2, th = threshold(im_th)
img, contours, _ = cv2.findContours(th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
contours_large = contour(th, contours)
print ("number of tags: %d" %len(contours_large))

im_copy = np.copy(im)
im_contours = cv2.drawContours(im_copy, contours_large, -1, (0,0,0),2)
show_img(im_contours)
cv2.imwrite(image_out_dir + "im_contours.jpg", im_contours)


"""
ret1, th1 = threshold1(im_th)
cv2.imwrite("output/th1.jpg", th1)

th2 = threshold2(im_th)
cv2.imwrite("output/th2.jpg", th2)
"""


"""#付箋数えるテストここから

im_copy = np.copy(im)
im_contours = cv2.drawContours(im_copy, contours_large, -1, (0,0,0),2)

cv2.imwrite("output/image-contour1.jpg", im_contours)
print ("number of tags: %d" %len(contours_large))

im_copy = np.copy(im)
for cnt in contours_large:
    x, y, w, h = cv2.boundingRect(cnt)
    bounding_img = cv2.rectangle(im_copy, (x, y), (x + w, y + h), (0, 255, 0), 3)

cv2.imwrite("output/image-bounding.jpg", bounding_img)

"""#ここまで



outputs = []
rects = []
approxes = []

for i,cnt in enumerate(contours_large):
    arclen = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.02*arclen, True)
    if len(approx) < 4:
        continue
    approxes.append(approx)
    rect = getRectByPoints(approx)
    rects.append(rect)
    outputs.append(getPartImageByRect(rect))
    cv2.imwrite(image_out_dir+str(i)+'.jpg', getPartImageByRect(rect))
