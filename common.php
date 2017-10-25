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
    $username = 'yuito';
    $password = 'panth1216';

    $options = [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
    ];

    return new PDO($dsn, $username, $password, $options);
}

/**
 * insert
 * @param string $sql
 * @param array $arr
 * @return int lastInsertId
 */
function insert($sql, $arr = []){
   $pdo = connect_db();
   $stmt = $pdo->prepare($sql);
   $stmt->execute($arr);
   return $pdo->lastInsertId();
}

/**
 * select
 * @param string $sql
 * @param array $arr
 * @return array $rows
 */
function select($sql){
   $pdo = connect_db();
   $stmt = $pdo->query($sql);
   if(!$stmt){
     $info = $pdo->errorInfo();
     exit($info[2]);
   }
   return $stmt->fetch();
}

/**
 * htmlspecialchars
 * @param string $string
 * @return $string
 */
function h($string){
   return htmlspecialchars($string, ENT_QUOTES, 'utf-8');
}

?>
