# 日報アプリ

## 概要

　このアプリケーションの目的は、"日報をYWT形式で、手軽に作成する"ことです。

　日報、特に新人が書く日報において重要なものは、「その日何を学び」、そして「つぎにどう生かすのか」という点です。
実際にどのような作業をどれだけしたかという内容の重要度はそれほど高くありません。

　しかしながら、その作業内容の記入に時間がとられることも事実です。
私の場合は、いつ、何を、どれだけしたのか思い出すことに最も時間をとられます。

　そこで、本アプリケーションは簡単なタスク管理と連携させることで、「思い出す」のではなく「思い出させる」日報を目指しました。

## 特徴

### 特徴

　以下に画面の例を示します。画面の構成は、基本的に日報の情報画面(左側)とタスク管理画面(右側)から成り立ちます。
日報情報画面に関しては、一般的な日報アプリケーションに対するイメージで問題なく動作すると思います。

![toppage](https://github.com/hayashizakitakaaki/Introduction_mysite/blob/images/docs/images/04_top_01.PNG "toppage")

　タスク管理画面は大きく"今日のタスク"と"明日のタスク"の二つに分かれていますが、それぞれの要素は共通です。

　タスクは以下の要素から成り立ちます。

* 作業の完了状態
* 実施日
* タスク名、または作業概要
* 予定作業時間
* 実際の作業にかかった時間

　基本的には前日の日報を書く際に、または日報を書く前に、あらかじめタスクを登録し、当日はそのタスクに対して、
「実際に何時間行ったか」「作業自体は終わったか」という点を登録します。
もちろん、当日突発的に起こった作業の登録も可能です。

　同時に、明日行うタスク、または明日以降に行う予定となっているタスクを登録していきます。
ここも登録する内容は今日のタスクに登録する際と同じです。
入力する必要のある情報は少なく、特に悩むことなく埋められる項目ばかりであり、それほど負担にもなりません。

　これらをこなしつつ、一日の作業が終わったら"新規投稿"ボタンを押しましょう。

　そこには、あなたが今日行った作業、つまり"やったこと"と、明日以降行う予定の作業、つまり"つぎにやること"が入力された状態であるはずです。

　ここまでくれば、あなたがすることは、残りの"わかったこと"を埋めるだけです。

　もちろん、"やったこと"、"つぎにやること"に対してコメントを入れることもできます。

　時間内に終わらなかったり、その日の内に終わらなかったようなタスクがあるのであれば、
その原因について考え、"やったこと"、"つぎにやること"のコメント欄に記入してみましょう。

　この特徴により、あなたが日報を書くのにかけている時間が5分短くなるでしょう(当社比)。

### 機能

　このアプリケーションは実装済みの機能として以下を持ちます。

* 日報管理
    * 投稿、編集、削除、閲覧
* コメント管理
    * 投稿、編集、削除、閲覧(日報詳細画面に表示)
* タスク管理
    * 登録、タスク完了状態の変更、実績時間の登録、その他全項目の修正
* ユーザー管理
    * ユーザー登録(必須：ユーザーネーム(ID)、姓、名、パスワード)
    * ユーザー情報の編集(ユーザーネーム、姓、名)
    * ログインしていない場合、全ページからログイン画面へリダイレクト
    * 異なるユーザーの投稿内容の編集はできない
* 表示関連
  * 日報一覧表示、日報詳細画面でのコメント閲覧・投稿、タスク一覧画面での閲覧・修正、ユーザー情報の閲覧・編集
  * ユーザー検索機能、日報検索機能(OR検索)、日報絞込み機能(日付、ユーザー)、タスク絞込み機能(日付、完了状態)
  * マークダウン表示への対応(日報YWT部分、コメント)

　このアプリケーションは、実装予定の機能として以下を考えています。

* タスク単位の目標管理
    * 目標、及び目標の達成状態を基本とする想定
        * モデルには作成済み
        * 達成状態の理由については、各日報のコメント欄を使用することを想定
* ユーザー情報項目の追加
    * 所属、自己紹介、その他
* ユーザーパスワードの修正機能

## 使い方

  ユーザー登録、タスクの追加、日報の投稿、コメントの投稿という基本的な流れの操作方法を示します。
  
### ユーザー登録・編集

　以下に、ログインページの画像を示します。登録するには右下の「ユーザー登録」ボタンを押してください。

![loginpage](https://github.com/hayashizakitakaaki/Introduction_mysite/blob/images/docs/images/01_login_01.PNG "loginpage")

　以下がユーザー登録画面です。入力項目はユーザー名(=ユーザーID)、姓、名、パスワードです。
ユーザー名は一意である必要があります。また、パスワードが異なるとコメントが表示されます。
無事、登録が完了するとログインページにリダイレクトされます。登録したユーザー名、パスワードを入力し、ログインボタンを押してください。

![resisterpage](https://github.com/hayashizakitakaaki/Introduction_mysite/blob/images/docs/images/02_register_01.PNG "resisterpage")

### タスクの追加・編集

　以下がログイン直後の画面です。タスクを登録する際に必須の情報は、実施日、作業内容、予定時間です。作業が完了したのであれば、実務時間の項目を埋め、チェックを入れて「更新」ボタンを押してください。ただし、作業したものの完了しなかったという場合には、チェックを入れる必要はないでしょう。

　基本的に、タスクの把握という意味で作業前の登録を推奨しますが、作業後の登録ももちろん可能です。その際には、作業の完了状態(チェックボックス)、と実作業時間についても記入するべきです。

![toppage](https://github.com/hayashizakitakaaki/Introduction_mysite/blob/images/docs/images/04_top_01.PNG "toppage")

　画面上部の「絞り込み」ボタン、または「すべて表示」ボタンをクリックすると、タスクの一覧画面に移動します。「絞り込み」を行っていた場合には、その条件に従った絞り込み結果が表示されます。このページではタスクのすべての項目が編集可能な状態となっています。また、削除したいタスクがあったら、「削除」の右にあるチェックボックスにチェックを入れ、更新ボタンを押してください。

　注意事項として、既存のタスクを編集し、更新する際には「更新」ボタンを、新規にタスクを登録する際には「登録」ボタンを使用してください。対応するボタンを使用しない場合、編集内容が正常に適用されません。

![taskpage](https://github.com/hayashizakitakaaki/Introduction_mysite/blob/images/docs/images/07_task_01.PNG "taskpage")

### 日報の投稿

　日報を投稿するには、ナビゲーションバー(画面上)上の「新規投稿」リンク、または画面内の「新規投稿」ボタンをクリックしてください。日報の編集画面を以下に示します。

![editpage](https://github.com/hayashizakitakaaki/Introduction_mysite/blob/images/docs/images/06_dailyedit_01.PNG "editpage")

　"やったこと"、"つぎにやること"にタスクが既に登録されていることが確認できるはずです。タスクの情報について、すでに入力してあることが理想ですが、後から追加することも可能です。その際は、画面下部の「保存してタスクの編集へ」ボタンをクリックしてください。

　日報のYWTを入力する欄はマークダウン記法での入力に対応しています。必要があれば利用してください。

　作成した日報を投稿し、公開するには「公開」ボタンを押してください。「保存してタスクの編集へ」、「プレビュー」ボタンを押すと、日報を非公開としていったん保存し、それぞれの画面に移動します。移動先での用事を済ませたら、再度編集し、日報を公開しましょう。非公開の日報を編集するには、自分の投稿一覧から選択するか、プレビュー画面から移動することができます。もちろん、すでに公開済みの日報を編集することも可能です。ただし、公開済みの日報を非公開状態に戻すことはできません。

　日報を削除したいのであれば、自分の投稿一覧のページに移動し、一覧の項目それぞれに表示されている「削除」ボタンをクリックしてください。表示されるアラートで「OK」をクリックすると削除されます。

![userpage](https://github.com/hayashizakitakaaki/Introduction_mysite/blob/images/docs/images/08_daily_01.PNG "userpage")

### コメントの投稿

　以下にコメント画面を示します。日報の詳細欄の下にあるのが、その日報に対して投稿されたコメントの一覧、そしてコメントの投稿欄です。欄内にコメントを入力し、投稿ボタンを押すことで、日報に対してコメントを投稿することができます。このコメント欄の入力もマークダウン記法に対応しています。

　自分の投稿したコメントには「編集」ボタンと「削除」ボタンが表示されています。「編集」ボタンを押すとコメントの編集を行うためのページに移動し、編集することができます。そのページで「投稿」ボタンを押すことで、その編集を適用することができます。

　「削除」ボタンを押すと、コメントを削除するかどうかというアラートが表示されます。そこで「OK」をクリックすると削除完了です。

![commentpage](https://github.com/hayashizakitakaaki/Introduction_mysite/blob/images/docs/images/11_detail_01.png "commentpage")

## 開発環境の設定

### 動作環境

　開発環境は以下の通りです。
* windows7 32bit
* python 3.5.1
* django 1.8.13
* postgreSQL 9.6

　また、pythonのモジュールとして、以下を使用しています。requirements.txtから導入してください。psycopg2に関しては、windowsの場合インストーラが提供されていますので、そちらをダウンロードの上、インストールしてください。
* django-bootstrap-form 3.2.1
* django-markdown-deux 1.0.5
* django-pure-pagination 0.3.0
* psycopg2 2.6.1

### 初期設定

#### データベースの設定

　データベースの設定を行います。手順としては、postgreSQLのデータベースを作成し、アプリケーションの"settings.py"に設定するというものになります。

　まず、コマンドライン上でpostgreSQLのデータベースに接続してください。以下は、windows環境でpostgreSQLを設定を変更せずにインストールした場合の、データベースに対して全権限を持つユーザー(postgres)で接続する方法です。
~~~
> psql postgres postgres
~~~
　接続後、アプリケーションで使用するユーザーとデータベースの作成を行います。以下のコマンドを順番に入力してください。"user"および"databasename"、"password"には、それぞれ設定したい名称を入力してください。
~~~
> CREATE USER user;
> ALTER ROLE user WITH PASSWORD 'password';
> CREATE DATABASE databasename OWNER user;
~~~
　以上で、データベースの作成は終了です。次に、アプリケーションにデータベースを設定します。以下のファイルを開き、各項目を入力します。
~~~
Introduction_mysite/ex_password.dummy.py
~~~
　上から順に、データベースオーナーユーザーのパスワード、データベースのオーナーユーザー名、データベースの名前、そしてdjangoのシークレットキーです。以下に例を示します。djangoのシークレットキーは一意に識別することが目的ですので、適度な長さの文字列で構いません。
~~~
database_password = 'password'
database_user = 'django'
database_name = 'django'
secret_key = '^#ugn5-vl6%n!^7p)cqsh8c&zag3y1=(a3#g4)!1b0dlb0a0jf'
~~~
　最後に、ファイルの名前から`ex_password.dummy.py`から、`.dummy`を削除することで、データベースの設定は完了です。

#### django初期設定

　次に、データベースをマイグレートします。マイグレーションファイルを作成する必要があるアプリはaccountsとcmsの二つです。manage.pyのある階層に移動し、それぞれ以下のコマンドでマイグレーションファイルを生成してください。
~~~
> python manage.py makemigrations accounts
> python manage.py makemigrations cms
~~~
　それが終わったらデータベースをマイグレートしましょう。コマンドは以下の通りです。
~~~
> python manage.py migrate
~~~
　これでデータベースにモデルを適用することができました。つぎに、管理ユーザーの作成を行います。コマンドは以下の通りです。
~~~
> python manage.py createsuperuser
~~~
　表示されるダイアログにユーザー名とパスワードを設定することで完了です。ここで作成したアカウントで本アプリケーションにログインすることができます。

　以上で初期設定は終了です。


### 実行方法

　アプリケーションを実行するには以下のコマンドをコマンドラインから入力してください。
~~~
> python manage.py runserver
~~~
　実行後、以下のアドレスをWebブラウザに入力し、アプリケーションにアクセスします。
~~~
http://127.0.0.1:8000/login
~~~
　初期設定の際に登録した管理ユーザーでもログインすることができます。また、ユーザー登録、およびその後の使い方については、上記"使い方"を参照してください。

## バージョン情報

2016/6/15 v1.0 release(実質)
* 日報、コメント、ユーザー管理、日報検索

2016/9/12 v1.1 release
* タスク管理機能の追加、バグ修正、各種デザイン・レイアウトの修正

2016/9/13 v1.1.2 release
* requirements.txtの追加、エラー処理追加

## ライセンス

