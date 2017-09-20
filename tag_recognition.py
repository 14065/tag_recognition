import cv2
import numpy as np

#from sklearn.cluster import KMeans
#KMeans

image_dir = 'images/'
image_file = 'image3.JPG'
im = cv2.imread(image_dir + image_file, 1)
#im_th = (np.abs(im[:,:,2] - im[:,:,1]) + np.abs(im[:,:,2] - im[:,:,0]))
#cv2.imwrite("output2/im_th.jpg", im_th)
im_blur = cv2.GaussianBlur(im, (25,25), 0)
cv2.imwrite("output/im_blur.jpg", im_blur)
im_th = (np.abs(im_blur[:,:,2] - im_blur[:,:,1]) + np.abs(im_blur[:,:,2] - im_blur[:,:,0]))


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

#画像を２値化する関数255は固定
ret1, th1 = cv2.threshold(im_th, 127,255, cv2.THRESH_BINARY)
th2 = cv2.adaptiveThreshold(im_th, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11,3)
#付箋部分だけ取りたい時↓
ret2, th = cv2.threshold(im_th, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

cv2.imwrite("output/th2.jpg", th2)
cv2.imwrite("output/th.jpg", th)
cv2.imwrite("output/th1.jpg", th1)

img, contours, _ = cv2.findContours(th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
"""#contoursの表示
cv2.imshow("image",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""

# filtered with area over (all area / 100 )
th_area = im.shape[0] * im.shape[1] / 100
contours_large = list(filter(lambda c:cv2.contourArea(c) > th_area, contours))

print(len(contours_large))

#付箋数えるテストここから

im_copy = np.copy(im)
im_contours = cv2.drawContours(im_copy, contours_large, -1, (0,0,0),2)

cv2.imwrite("output/image-contour1.jpg", im_contours)
print ("number of tags: %d" %len(contours_large))

im_copy = np.copy(im)
for cnt in contours_large:
    x, y, w, h = cv2.boundingRect(cnt)
    bounding_img = cv2.rectangle(im_copy, (x, y), (x + w, y + h), (0, 255, 0), 3)

cv2.imwrite("output/image-bounding.jpg", bounding_img)

#ここまで

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
    cv2.imwrite('output/'+str(i)+'.jpg', getPartImageByRect(rect))


"""
#付箋の色でクラスタリング
t_colors = []
for i,out in enumerate(outputs):
    color = np.zeros(3)
    for j in range(3):
        color[j] = np.median(out[:,:,j])
    t_colors.append(color)
t_colors = np.array(t_colors)

cluster_num = 4
kmeans = KMeans(n_clusters = cluster_num).fit(t_colors)
labels = kmeans.labels_
centers = np.array(kmeans.cluster_centers_).astype(np.int)
"""
