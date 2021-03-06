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
  $id = $_GET["id"];

  $stmt = $pdo->prepare("SELECT * FROM changed_img WHERE id = ?");
  $stmt ->execute(array($id));

  if(!$stmt){
    $info = $pdo->errorInfo();
    exit($info[2]);
  }

  $data = $stmt->fetch(PDO::FETCH_ASSOC);
  header('Content-type: ' . $MIMETypes[$data['changed_img']]);
  #file_get_contents($data['changed_img']);
  echo $data['changed_img'];


} catch (Exception $e) {
echo "load failed: " . $e;
}
?>
