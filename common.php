<?php
/**
 * common.php
 */

/**
 * connect_db
 * @return \PDO
 */
function connect_db(){
    $dsn = 'mysql:host=localhost;dbname=tag;charset=utf8';
    $username = 'user';
    $password = 'pass';

    $options = [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
    ];

    return new PDO($dsn, $username, $password, $options);
}

/**
 * htmlspecialchars
 * @param string $string
 * @return $string
 */
function h($string){
   return htmlspecialchars($string, ENT_QUOTES, 'utf-8');
}

function get_time($id){
  $pdo = connect_db();

  $stmt = $pdo->prepare("SELECT * FROM changed_img WHERE id = ?");
  $stmt->execute(array($id));

  if(!$stmt){
    $info = $pdo->errorInfo();
    exit($info[2]);
  }
  return $stmt->fetch(PDO::FETCH_ASSOC);
}

function get_images($id){
  $pdo = connect_db();

  $sql = 'SELECT * FROM images WHERE id = ?';
  $stmt = $pdo->prepare($sql);
  $stmt->execute(array($id));
  if(!$stmt){
    $info = $pdo->errorInfo();
    exit($info[2]);
  }
  return $stmt->fetch(PDO::FETCH_ASSOC);
}

function get_latest_id(){
  $pdo = connect_db();

  $stmt = $pdo->prepare("SELECT * FROM images WHERE id = (SELECT MAX(id) FROM images)");
  $stmt->execute();

  if(!$stmt){
    $info = $pdo->errorInfo();
    exit($info[2]);
  }
  return $stmt->fetch(PDO::FETCH_ASSOC);

}

?>
