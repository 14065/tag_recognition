<?php

/* 設定 */
define('DATA_FILENAME', 'test.log');     // データファイル
define('DISP_MAX',  10);                 // 1ページの最大表示数
define('LIMIT_SEC', 5);                  // 連続投稿を禁止する秒数
define('TOKEN_MAX', 10);                 // ワンタイムトークン蓄積最大数
define('SESSION_NAME', 'MiniBoard');     // セッションクッキーに用いる名前
date_default_timezone_set('Asia/Tokyo'); // タイムゾーン
mb_internal_encoding('UTF-8');           // 内部エンコーディング

/**
 * HTML特殊文字をエスケープする関数
 */
function h($str) {
    return htmlspecialchars($str, ENT_QUOTES, 'UTF-8');
}

/**
 * RuntimeExceptionを生成する関数
 * http://qiita.com/mpyw/items/6bd99ff62571c02feaa1
 */
function e($msg, Exception &$previous = null) {
    return new RuntimeException($msg, 0, $previous);
}

/**
 * 例外スタックのメッセージ部分を配列に変換する関数
 * http://qiita.com/mpyw/items/6bd99ff62571c02feaa1
 */
function exception_to_array(Exception $e) {
    do {
        $msgs[] = $e->getMessage();
    } while ($e = $e->getPrevious());
    return array_reverse($msgs);
}

/* 変数の初期化 */
// リクエストパラメータをトリミングした後展開
foreach (array('name', 'text', 'token', 'page', 'submit') as $v) {
    $$v = isset($_REQUEST[$v]) && is_string($_REQUEST[$v]) ? trim($_REQUEST[$v]) : '';
}
// ページ番号を1以上の整数になるように補正
$page = max(1, (int)$page);

/* セッションの初期化 */
session_name(SESSION_NAME); // セッション名を設定
@session_start();           // セッション開始
// セッション変数を初期化
if (!$_SESSION) {
    $_SESSION = array(
        'name'  => '',
        'text'  => '',
        'token' => array(),
        'prev'  => null,
    );
}

/* データファイルに関する処理 */
try {
    // データファイルを読み書き両用でオープン
    // (ポインタを先頭にセット, 未作成ならば新規作成)
    if (!$fp = @fopen(DATA_FILENAME, 'a+b')) {
        throw e('データファイルのオープンに失敗しました。', $e);
    }
    // データファイルを共有ロック
    flock($fp, LOCK_SH);
    // ファイルを読み取ってシリアルからの復元を試みる
    $articles = @unserialize(stream_get_contents($fp)) ?: array();
    // 送信ボタンが押された場合
    if ($submit) {
        try {
            // セッション変数に書き込む情報をセット
            $_SESSION['name'] = $name;
            $_SESSION['text'] = $text;
            // ワンタイムトークンが直近指定個に含まれていなければ弾く
            if (!isset($_SESSION['token'][$token])) {
                throw e('フォームの有効期限が切れています。', $e);
            }
            // ワンタイムトークンを消費させる
            unset($_SESSION['token'][$token]);
            // 最後の投稿から指定秒経過していなければ弾く
            if ($_SESSION['prev'] !== null) {
                $diff = $_SERVER['REQUEST_TIME'] - $_SESSION['prev'];
                if (($limit = LIMIT_SEC - $diff) > 0) {
                    throw e("投稿間隔が短すぎます。あと{$limit}秒ほどお待ちください。", $e);
                }
            }
            // 名前をチェック
            if (!$len = mb_strlen($name) or $len > 30) {
                $e = e('名前は30字以下で入力してください。', $e);
            }
            // 本文をチェック
            if (!$len = mb_strlen($text) or $len > 140) {
                $e = e('本文は140字以下で入力してください。', $e);
            }
            // 例外がここまでに1つでも発生していればスローする
            if (!empty($e)) {
                throw $e;
            }
            // 排他ロックに切り替える
            flock($fp, LOCK_EX);
            // 配列の先頭にデータを追加
            array_unshift($articles, array(
                'name'  => $name,
                'text'  => $text,
                'time'  => date('Y-m-d H:i:s', $_SERVER['REQUEST_TIME']),
            ));
            // ファイルを空にする
            ftruncate($fp, 0);
            // 編集した配列をシリアル化して上書き
            fwrite($fp, serialize($articles));
            // セッションに時間を記録し、メッセージをセット
            $_SESSION['prev'] = $_SERVER['REQUEST_TIME'];
            // フォームの投稿内容をリセットする
            $_SESSION['text'] = '';
            // 正しい処理を行ったが、形式上例外としてスロー
            throw e('書き込みました', $e);
        } catch (Exception $e) { }
    }
    // 総件数をセット
    $whole_count = count($articles);
    // 総ページ数をセット
    $page_count = ceil($whole_count / DISP_MAX);
    // ページ番号にあった分だけ取り出す
    $articles = array_slice($articles, ($page - 1) * DISP_MAX);
    // 現在のページの件数をセット
    $current_count = count($articles);
} catch (Exception $e) { }
// 後始末
if (!empty($fp)) {
    flock($fp, LOCK_UN);
    fclose($fp);
}

/* ワンタイムトークンを次の投稿のために準備 */
$_SESSION['token'] = array_slice(
    array($token = sha1(mt_rand()) => 1) + $_SESSION['token'],
    0,
    TOKEN_MAX
);

/* ヘッダー送信 */
header('Content-Type: application/xhtml+xml; charset=utf-8');

?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>ミニ掲示板</title>
    <style type="text/css"><![CDATA[
    <!--
    #wrapper {
      width: 100%;
    }
    #header, #container, #footer {
      width: 650px;
      margin: 0px auto;
    }
    #header, #footer {
      text-align: center;
    }
    #messages, #textarea, #articles {
      width: 550px;
      margin: -3px auto 0px;
      border-top: 3px double black;
      padding: 5px;
    }
    #articles {
      overflow: hidden;
      padding-top: 1px;
    }
    .article {
      margin-top:-1px;
      border-top: 1px dotted black;
      padding: 1px;
    }
    .article_name {
      font-size: 20px;
    }
    .article_text {
      margin: 10px;
    }
    .article_time {
      text-align: right;
      font-size: 11px;
    }
    .page {
      font-size: 15px;
      text-align: right;
    }
    body {
      background: white;
    }
    h1 {
      color: black;
    }
    textarea {
      width: 100%;
      height: 20px;
    }
    label {
      display: block;
      margin: 1px 1px;
    }
    -->
 ]]></style>
  </head>
  <body>
  <a href="main.php" target="_top"><input type="button" value="メイン画面に戻る"></input></a>
    <div id="wrapper">
      <div id="header">
        <h1>～ミニ掲示板～</h1>
      </div>
      <div id="container">
        <div id="textarea">
          <form action="" method="post">
            <label>名前: <input name="name" type="text" value="<?=h($_SESSION['name'])?>" /></label>
            <label>本文<p><textarea name="text"><?=h($_SESSION['text'])?></textarea></p></label>
            <label style="text-align:right;"><input type="submit" name="submit" value="投稿" /></label>
            <label><input type="hidden" name="token" value="<?=h($token)?>" /></label>
          </form>
        </div>
<?php if (!empty($e)): ?>
        <div id="messages">
<?php foreach (exception_to_array($e) as $msg): ?>
          <div><?=h($msg)?></div>
<?php endforeach; ?>
        </div>
<?php endif; ?>
<?php if (!empty($articles)): ?>
        <div id="articles">
<?php foreach ($articles as $article): ?>
          <div class="article">
            <div class="article_name"><?=h('@'.$article['name'])?></div>
            <div class="article_text"><pre><?=h($article['text'])?></pre></div>
            <div class="article_time"><?=h($article['time'])?></div>
          </div>
<?php endforeach; ?>
        </div>
<?php endif; ?>
      </div>
      <div id="footer">
        <div>
<?php if ($page > 1): ?>
          <a href="?page=<?=$page-1?>">前</a> |
<?php endif; ?>
          <a href="?">最新</a>
<?php if (!empty($page_count) and $page < $page_count): ?>
           | <a href="?page=<?=$page+1?>">次</a>
<?php endif; ?>
        </div>
        <p class="page"><?php
          if (empty($current_count)) {
            echo 'まだ書き込みはありません';
          } else {
            printf('%d件中%d件目～%d件目(%dページ中%dページ目)を表示中',
              $whole_count,
              ($tmp = ($page - 1) * DISP_MAX) + 1,
              $tmp + $current_count,
              $page_count,
              $page
            );
          }
        ?></p>
      </div>
    </div>
  </body>
</html>
