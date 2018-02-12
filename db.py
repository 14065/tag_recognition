import mysql.connector

connect = mysql.connector.connect(
    user = 'user',
    password = 'pass',
    host = 'localhost',
    db = 'tag',
    charset='utf8'
)

def db_images_insert(todo, doing, done, img):
    cursor = connect.cursor()

    sql = "INSERT INTO images(todo, doing, done, img) VALUES(%s, %s, %s, %s)"
    cursor.execute(sql, (todo, doing, done, img))

    connect.commit()

def db_tag_insert(num, x, y, img, area):
    cursor = connect.cursor()

    sql = "INSERT INTO tag_info(image_id, tag_id, midpoint_x, midpoint_y, tag_img, area)       VALUES((SELECT id FROM images WHERE id = (SELECT MAX(id) FROM images)),%s, %s, %s, %s, %s)"
    cursor.execute(sql, (num, x, y, img, area))

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

def get_num_of_previous_tag():
    cursor = connect.cursor(dictionary=True)

    sql = "SELECT * FROM images WHERE id = (SELECT MAX(id) FROM images)"
    cursor.execute(sql)
    row = cursor.fetchone()
    if row is not None:
        return row['todo'], row['doing'], row['done']
    else:
        return 99,99,99

def calc_time(image_id, tag_id):
    cursor = connect.cursor(dictionary=True)

    sql = "SELECT * FROM tag_info WHERE image_id = %s AND tag_id = %s"
    cursor.execute(sql, (image_id, tag_id))
    row = cursor.fetchone()
    upload = row['upload_at']
    update = row['updated_at']
    return update-upload

def update_time(image_id, tag_id, put_time):
    cursor = connect.cursor(dictionary=True)

    sql = "UPDATE tag_info SET put_time = %s WHERE image_id = %s AND tag_id = %s"
    cursor.execute(sql, (put_time, image_id, tag_id))

    connect.commit()

def calc_time_tag(image_id, tag_id):
    cursor = connect.cursor(dictionary=True)

    put_time = calc_time(image_id, tag_id)
    update_time(image_id, tag_id, put_time)

def calc_time_tag_stay(image_id, tag_id, tmp_midpoint, area):
    cursor = connect.cursor(dictionary=True, buffered=True)
    sql = "SELECT * FROM tag_info WHERE image_id = %s and area = %s and flag = 0"
    cursor.execute(sql, ((image_id-1), area))
    row = cursor.fetchone()
    if row is not None:
        while row is not None:
            from paint import tolerance_area

            mid_p = (row['midpoint_x'], row['midpoint_y'])
            #print('midpoint: %r' %((mid_p[0], mid_p[1]),))

            left, right, top, bottom = tolerance_area(mid_p)

            if left < tmp_midpoint[0] < right and top < tmp_midpoint[1] < bottom:
                put_time = calc_time(image_id, tag_id) + row['put_time']
                update_time(image_id, tag_id, put_time)
                break

            row = cursor.fetchone()
