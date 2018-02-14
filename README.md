# Step1 システム利用の準備

本システムはLinuxのUbuntuを利用して開発を行った．そのため，初めにOracle Vm Virtual BoxからUbuntuの仮想環境を構築するまでの流れの説明．開発で使用したPython，PHP，MySQLなどのインストールを行い，動作するまでの流れを説明する．

## Step1.1 仮想環境の構築

このステップでは，開発で使用したUbuntu 16.04 LTSの環境の構築を行う．

https://www.virtualbox.org/wiki/Downloads

からVirtual Boxバージョン5.2.0をインストールする

https://www.ubuntulinux.jp/download/ja-remix

から「ubuntu-ja-16.04-desktop-amd64.iso」をダウンロード



ダウンロードが終わったらVirtual Boxを起動する．

Oracle VM VirtualBox マネージャーの左上の「新規」をクリック

名前は自由，タイプは「Linux」，バージョンは「Ubuntu (64-bit)」．その後はメモリサイズやハードディスクに関する設定．ハードディスクは30GB以上に設定．あとは自由．

作成が終われば「新規」の横の「設定」をクリック

ストレージを選択し「コントローラー：IDE」の下にあるディスクマークをクリックすると，右側の属性に光学ドライブが表示されるので横のディスクマークをクリック．仮想光学ディスクファイルを選択をクリックし，先ほどダウンロードした「ubuntu-ja-16.04-desktop-amd64.iso」を選択．

コントローラー：IDEに選択したファイルが記入されていればOK．Ubuntuを起動する．



起動するとUbuntuをインストールを選択し，初期設定を行う．設定は自由．(ユーザ名は後の設定で使うので覚えておく) 

## Step1.2 Anacondaのインストール

このステップではAnacondaのインストールとパスの設定．OpenCV，mysql-connector-pythonのインストールを行う．

FireFoxから https://www.anaconda.com/download/  にアクセス

バージョン3.6をダウンロード

terminal を開き、~/ダウンロード に移動する

インストールする

```
$ bash Anaconda3-5.0.1-Linux-x86_64.sh
```

途中、以下を聞かれる

- ライセンス
  - yes で表示し、enter で文末までスクロール
- anaconda のインストールディレクトリ
  - デフォルト：/home/ユーザ名/anadonda3
- PATH に追加するか
  - デフォルト：yes

パスの設定

```
$ which curl
/usr/bin/curl
$ export PATH=/home/ユーザ名/anaconda3/bin:$PATH
$ which curl
~/anaconda3/bin/curl
```

確認する

conda のバージョン

```
$ conda -V
conda 4.3.30
```

Python のバージョンも確認しておく．

```
$ python -V
Python 3.6.3 :: Anaconda, Inc.
```

となればOK．



次にOpenCVとmysql-connector-pythonのインストール

`$ conda install --channel https://conda.anaconda.org/menpo opencv3`

`$ conda install -c https://conda.anaconda.org/anaconda mysql-connector-python`



## Step1.3 MySQLのインストール

このステップでは，MySQLのインストールとデータベースとテーブルの作成などを行う．

まず，MySQLをインストール

`$ sudo apt-get update`

でリポジトリの更新．

`$ sudo apt-get install mysql-server`

インストール中にパスワードを聞かれるのでメモする．

インストールが終われば`$ mysql -u root -p`でMySQLを起動．パスワードを聞かれるので，インストール時に聞かれたパスワードを打つ．

ログインができたら以下のコードをコピペし，ユーザの作成を行う．

``` 
$ GRANT ALL PRIVILEGES ON *.* TO user@localhost IDENTIFIED BY 'pass' WITH GRANT OPTION;
$ FLUSH PRIVILEGES;
```

MySQLのユーザ名はuser，パスワードはpassと設定したので次回のログインからは

`$ mysql -u user -p`

でパスワードは`pass`を入力しログインする．



次にデータベースの作成

`CREATE DATABASE tag;`でデータベースの作成．

作成が終われば`use tag;`で作成したデータベースに移動．

テーブルの作成．

imageテーブルの作成

```
CREATE TABLE `images` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `todo` int(11) DEFAULT NULL,
  `doing` int(11) DEFAULT NULL,
  `done` int(11) DEFAULT NULL,
  `img` longblob,
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

tag_info	の作成．

```
CREATE TABLE `tag_info` (
  `image_id` int(11) DEFAULT NULL,
  `tag_id` int(11) DEFAULT NULL,
  `midpoint_x` int(11) DEFAULT NULL,
  `midpoint_y` int(11) DEFAULT NULL,
  `tag_img` mediumblob,
  `upload_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `area` int(11) DEFAULT NULL,
  `flag` int(11) DEFAULT NULL,
  `put_time` time DEFAULT NULL,
  KEY `image_id` (`image_id`),
  CONSTRAINT `tag_info_ibfk_1` FOREIGN KEY (`image_id`) REFERENCES `images` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

changed_imgテーブルの作成．

```
CREATE TABLE `changed_img` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `changed_img` longblob,
  `time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

これでテーブルの作成は完了．



## Step1.4 ApacheとPHPのインストール

このステップではApacheとPHPのインストールと設定を行う．

#### apacheインストール

`$ sudo apt-get install apache2`

インストールが終われば，public_htmlフォルダをホームディレクトリに作成．

`$ sudo a2enmode userdir`

これによりホームディレクトリのpublic_htmlが公開される．



#### PHPのインストール

`$ sudo apt-get install php`

`$ sudo apt install php libapache2-mod-php`

`$ sudo apt install php-mysql`

`$ sudo apt-get install php-mbstring`

インストールが終われば

/etc/apache2/mods-available/php7.0.confの

`php_admin_flag engine Off` をコメントアウト．これで，上で設定したpublic_html内でPHPが使えるようになる．



/etc/php/7.0/apache2/php.ini の

`;extension=php_mbstring.dll`をコメントアウト

mbstringに関する項目を以下に設定する．

```
mbstring.language = Japanese

mbstring.internal_encoding = UTF-8

mbstring.http_input = pass

mbstring.http_output = pass

mbstring.encoding_translation = Off

mbstring.detect_order = UTF-8,SJIS,EUC-JP,JIS,ASCII

mbstring.substitute_character = none;
```

次に/etc/apache2/sites-available/000-default.confのDocumentRootと書かれている部分を以下に変更．

```
DocumentRoot /home/ユーザ名/public_html
<Directory /home/ユーザ名/public_html>
Options Indexes FollowSymLinks
AllowOverride None
Require all granted
</Directory>
```



終わったら`$ sudo service apache2 restart`でapache2を再起動．

`http://localhost/`にアクセスできるか確認．



以上で準備完了となる．

# Step2 システムの利用方法

このステップでは，システムの起動方法などを説明する．

https://github.com/14065/tag_recognition

上のリンクからリポジトリをクローンする．

PCにカメラを接続し，Virtual Box のウィンドウの「デバイス」→「Webカメラ」から使用するカメラを選択することでそのカメラがVirtual Box内で使用することができる．ただし，ホスト側でカメラを使用している場合，Virtual Box内で認識されないので注意．



`$ python tag_recognition.py`で実行し，カメラの写真が写れば正常に動作している．

Webページへのアクセスは`localhost/main.php`でアクセスできる．



参考

https://qiita.com/sugurunatsuno/items/ce3c0d486bdc93688192

https://qiita.com/t2y/items/2a3eb58103e85d8064b6

https://qiita.com/january108/items/f4d0b655062a7c52e4fe

https://qiita.com/hiroq/items/d6f611791ae2124f0fbe

http://charlie1012.hatenablog.jp/entry/2015/09/05/170000

https://qiita.com/suppy193/items/84153ce3c70deb89c37a

https://qiita.com/zaburo/items/55347181be742b5109ea

http://kzlog.picoaccel.com/post-880/

http://d.hatena.ne.jp/iroiro-memo/20131130/1391097092
