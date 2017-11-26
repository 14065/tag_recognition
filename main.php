<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8">
<title>メイン画面</title>
</head>
<body>
<?php
require 'common.php';
try{
  $data = get_latest_time();
  $row = get_latest_images();

?>
  <img src="img_show.php" width="640" height="480"><br>
<?php
  echo $data['time'].' 更新<br>';
  echo 'Todoの付箋の枚数 : ' .$row['todo']. '枚  <br>';
  echo 'Doingの付箋の枚数: ' .$row['doing']. '枚  <br>';
  echo 'Doneの付箋の枚数 : ' .$row['done']. '枚  <br>';

  $pdo = null;

}catch(PDOException $e){
  print('Error: ') .$e->getMessage();
}
?>

<br><br><br>
<a href="img_up.php"><input type="button" value="画像を登録する"></a>

<a href="history.php"><input type="button" value="今までの履歴を見る"></a>
</body>
</html>
