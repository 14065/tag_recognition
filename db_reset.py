import mysql.connector

connect = mysql.connector.connect(
    user = 'user',
    password = 'pass',
    host = 'localhost',
    db = 'tag',
    charset = 'utf8'
)

cursor = connect.cursor(buffered=True)

sql = "DELETE FROM images; DELETE FROM tag_info; DELETE FROM changed_img; ALTER TABLE images AUTO_INCREMENT = 1; ALTER TABLE changed_img AUTO_INCREMENT = 1;"
#このまま実行してもリセットされない場合がある、その時は下のTrueをFalseにして実行してからTrueにする
cursor.execute(sql, multi = True)
connect.commit()
