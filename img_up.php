<html>
<head>
  <meta charset="utf-8">
  <title>画像登録ページ</title>
</head>
<body>
  <form method="post" enctype="multipart/form-data" action="img_up.php">
    <p>画像登録＆アップロード</p>
    <p>更新(f5)をすると画像が送信されてしまいます。</p>
    画像パス：<input type="file" name="image" size="30">
    <input type="submit" name="submit" value="送信"><br>
  </form>
  <a href="">


<?php
require'common.php';

if(isset($_FILES["image"])){
  $img = file_get_contents($_FILES["image"]["tmp_name"]);

/* test2.php用
  $pdo = new PDO('mysql: host=localhost; dbname=test_db; charset=utf8', 'yuito', 'panth1216');
*/

  $pdo = connect_db();
/* test.php用
  $pdo = new PDO('mysql: host=localhost; dbname=tag; charset=utf8', 'yuito', 'panth1216');
*/

# test2.php用
  #$sql = "INSERT INTO IMAGES(IMG) VALUES (?)";

# test.php用
  $sql = "INSERT INTO images(img) VALUES (?)";
  $stmt = insert($sql, [$img]);

  echo "登録が終了しました<br>";
}
?>

<a href="main.php"><input type="button" value="メイン画面に行く"></a>

</body>
</html>
