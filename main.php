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
  $id = $_GET["id"];
  $row = get_images($id);
  $data = get_time($id);

?>
  <img src="img_show.php?id=<?php echo $row['id'];?>" width="640" height="480"><br>
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

<br><br>
<?php if($row['id'] > 1){?>
  <a href="main.php?id=<?php echo ($row['id']-1);?>"><input type="button" value="前の画像"></a>
<?php }
$next = get_images($row['id']+1);
if($next){ ?>
  <a href="main.php?id=<?php echo ($row['id']+1);?>"><input type="button" value="次の画像"></a>
<?php } ?>
<a href="main.php?id=<?php echo get_latest_id()['id'];?>"><input type="button" value="最新の画像"></a>
<br>
<a href="history.php" target="_top"><input type="button" value="今までの履歴を見る"></a>
<a href="retrospective.html"><input type="button" value="掲示板にいく"></a>
</body>
</html>
