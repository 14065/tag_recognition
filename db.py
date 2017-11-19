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

def last_image_id():
    cursor = connect.cursor(dictionary=True)

    sql = "SELECT MAX(id) FROM images"
    cursor.execute(sql)

    max_id = cursor.fetchone()

    return max_id['MAX(id)']

def count_id(image_id):
    cursor = connect.cursor(dictionary=True)

    sql = "SELECT COUNT(tag_img) FROM tag_info WHERE image_id = %s" %image_id

    cursor.execute(sql)
    num = cursor.fetchone()

    return num['COUNT(tag_img)']+1
