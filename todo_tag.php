<html>
<head>
  <meta charset="utf-8">
  <title>履歴ページ</title>
</head>
<body>
  <h3>Todoにあったタスクのかかった時間</h3>
<table border="1" width="65%">
    <tr>
        <th>画像</th>
        <th>時間</th>
    </tr>
<?php
require 'common.php';

try{
  $pdo = connect_db();

  $sql = 'SELECT * FROM tag_info WHERE flag = 1 AND area = 1';
  $stmt = $pdo->query($sql);
  if(!$stmt){
    $info = $pdo->errorInfo();
    exit($info[2]);
  }

  while($row = $stmt->fetch(PDO::FETCH_ASSOC)){
    echo '<tr align=center>';
?>
    <td><img src="tag_show.php?imageid=<?php echo $row['image_id'];?>&tagid=<?php echo $row['tag_id'];?>" width="80" height="80"></td>

<?php
    echo '<td>' .$row['put_time']. '</td>';
    echo '</tr>';
  }
  echo '</table>';
  $pdo = null;
}catch(PDOException $e){
  print('Error: ' .$e->getMessage());
}
?>

</body>
</html>
