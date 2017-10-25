<html>
<head>
  <meta charset="utf-8">
  <title>履歴ページ</title>
</head>
<body>
<a href="main.php"><input type="button" value="戻る">
<table border="1" width="65%">
    <tr>
        <th>ID</th>
        <th>Todo</th>
        <th>Doing</th>
        <th>Done</th>
        <th>貼った画像</th>
        <th>貼った時間</th>
    </tr>
<?php
require 'common.php';

try{
  $pdo = connect_db();

  $sql = 'SELECT * FROM images';
  $stmt = $pdo->query($sql);
  if(!$stmt){
    $info = $pdo->errorInfo();
    exit($info[2]);
  }
  $row_count = $stmt->rowCount();
  echo 'レコード件数: ' .$row_count. "<br>";
  while($row = $stmt->fetch(PDO::FETCH_ASSOC)){
    echo '<tr align=center>';
    echo '<td>' .$row['id']. '</td>';
    echo '<td>' .$row['todo']. '</td>';
    echo '<td>' .$row['doing']. '</td>';
    echo '<td>' .$row['done']. '</td>';
?>
    <td><img src="img_show.php?id=<?php echo $row['id'];?> width="480" height="270""></td>

<?php
    echo '<td>' .$row['time']. '</td>';
    echo '</tr>';
  }
  echo '</table>';
  $pdo = null;
}catch(PDOException $e){
  print('Error: ' .$e->getMessage());
}
?>

<a href="main.php"><input type="button" value="戻る">
</a>
</body>
</html>
