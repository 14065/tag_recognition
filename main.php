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
  $pdo = connect_db();
  $sql = 'SELECT * FROM images WHERE id=(SELECT MAX(ID) FROM images)';
  $stmt = $pdo->query($sql);
  if(!$stmt){
    $info = $pdo->errorInfo();
    exit($info[2]);
  }

  while($row = $stmt->fetch(PDO::FETCH_ASSOC)){
?>
    <img src="img_show.php?id=<?php echo $row['id']; ?> width="640" height="480""><br>
<?php
    echo 'Todoの付箋の枚数 : ' .$row['todo']. '枚  <br>';
    echo 'Doingの付箋の枚数: ' .$row['doing']. '枚  <br>';
    echo 'Doneの付箋の枚数 : ' .$row['done']. '枚  <br>';
    }
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
