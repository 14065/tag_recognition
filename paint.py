import cv2
import numpy as np

image_dir = 'images/'
image_file = 'image5.JPG'
image_out_dir = "output/"

def each_area_get(image):
    height, width = image.shape[:2]
    todo_width = width // 3
    doing_width = 2 * width // 3

    todo_im = image[0:height, 0:todo_width]
    #cv2.imwrite("output/todo_im.jpg", todo_im)

    doing_im = image[0:height, todo_width:doing_width]
    #cv2.imwrite("output/doing_im.jpg", doing_im)

    done_im = image[0:height, doing_width:width]
    #cv2.imwrite("output/done_im.jpg", done_im)

    return todo_im, doing_im, done_im

def image_pre(im):
    im_th = (np.abs(im[:,:,2] - im[:,:,1]) + np.abs(im[:,:,2] - im[:,:,0]))

    im_blur = cv2.GaussianBlur(im_th, (25,25), 0)
    return im_blur

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
    area = im.shape[0] * im.shape[1] / 1000
    contours_large = list(filter(lambda c:cv2.contourArea(c) > area, contours))
    return contours_large

def show_img(img):
    cv2.imshow("image",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
