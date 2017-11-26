import mysql.connector
from paint import *

connect = mysql.connector.connect(
    user = 'yuito',
    password = 'panth1216',
    host = 'localhost',
    db = 'tag',
    charset='utf8'
)

def db_images_insert(todo, doing, done, img):
    cursor = connect.cursor()

    sql = "INSERT INTO images(todo, doing, done, img) VALUES(%s, %s, %s, %s)"
    cursor.execute(sql, (todo, doing, done, img))

    connect.commit()

def db_tag_insert(num, x, y, img):
    cursor = connect.cursor()

    sql = "INSERT INTO tag_info(image_id, tag_id, midpoint_x, midpoint_y, tag_img)       VALUES((SELECT id FROM images WHERE id = (SELECT MAX(id) FROM images)),%s, %s, %s, %s)"
    cursor.execute(sql, (num, x, y, img))

    connect.commit()

def db_changed_img_insert(img):
    cursor = connect.cursor()

    sql = "INSERT INTO changed_img(changed_img) VALUES(%s)"
    cursor.execute(sql, (img,))
    connect.commit()

def db_flag_update(image_id, tag_id, flag):
    cursor = connect.cursor()

    sql = "UPDATE tag_info SET flag=%s WHERE image_id = %s AND tag_id = %s"
    cursor.execute(sql, (flag, image_id, tag_id))
    connect.commit()

def last_image_id():
    cursor = connect.cursor(dictionary=True)

    sql = "SELECT MAX(id) FROM images"
    cursor.execute(sql)

    max_id = cursor.fetchone()

    return max_id['MAX(id)']

def get_last_image():
    cursor = connect.cursor(dictionary=True)
    id_num = last_image_id()

    sql = "SELECT * FROM images WHERE id = %s" %id_num
    cursor.execute(sql)
    row = cursor.fetchone()
    img = decode_img(row['img'])

    return img

def get_tmp_tag():
    cursor = connect.cursor(dictionary=True)
    id_num = last_image_id()

    sql = "SELECT * FROM tag_info WHERE image_id = %s" %(id_num-1)
    cursor.execute(sql)
    row = cursor.fetchone()

    tmp = decode_img(row['tag_img'])
    tmp_gray = cv2.cvtColor(tmp, cv2.COLOR_BGR2GRAY)

    return tmp_gray
