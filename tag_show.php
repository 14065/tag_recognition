<?php
require 'common.php';
$MIMETypes = array(
  'jpg' => 'image/jpeg',
  'png' => 'image/png',
  'jpeg' => 'image/jpeg',
  'gif'  => 'image/gif',
  'bmp'  => 'image/bmp',
  'JPG' => 'image/JPG',
);
try{
  $pdo = connect_db();
  $imageid = $_GET["imageid"];
  $tagid = $_GET["tagid"];
  $stmt = $pdo->prepare("SELECT * FROM tag_info WHERE image_id = ? and tag_id = ?");
  $stmt->execute(array($imageid, $tagid));
  if(!$stmt){
    $info = $pdo->errorInfo();
    exit($info[2]);
  }
  $data = $stmt->fetch(PDO::FETCH_ASSOC);
  header('Content-type: ' . $MIMETypes[$data['tag_img']]);
  file_get_contents($data['tag_img']);
  echo $data['tag_img'];
} catch (Exception $e) {
echo "load failed: " . $e;
}
?>
