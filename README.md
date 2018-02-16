コイン投げ器
============

画像の収集
----------

## 作業

- uploader.py

  画像を収集するマシンで実行します。
  raspberry_pi/toss_and_capture.py から送られてきた画像を upload_files に格納します。

  設定

    - host='0.0.0.0' および port=8080 を適宜変更します。

  実行

      python3 uploader.py

- raspberry_pi/toss_and_capture.py

  Raspberry Pi で実行します。
  コイン投げを行い、撮影した画像を uploader.py に送ります。

  設定

    - UPLOAD_URL を uploader.py を実行するマシンにあわせて修正します。

    - TRY_COUNT を適宜設定します。

      ※連続して動作させているとサーボから異音がすることがあったので、
      適宜、休ませながら行いました。

  実行

      python3 toss_and_capture.py

## ディレクトリ

- upload_files

  uploader.py で受信した画像を格納します。

画像の格納
----------

## 作業

  upload_files の画像を orig_imgs へ手作業でコピーします。

## ディレクトリ

- orig_imgs

コイン画像の抽出
----------------

## 作業

- make_coin_imgs.py

  orig_imgs の画像から、コイン画像のみ抽出し、coin_imgs に格納します。

  実行

      python3 make_coin_imgs.py

  その他

    うまく抽出できない場合、common.py の class CoinImage の get_img 関数で
    cv2.HoughCircles 呼び出しの引数 param1 および param2 を調整します。

## ディレクトリ

- coin_imgs

  make_coin_imgs.py が抽出したコイン画像を格納します。

コイン画像を手作業で分類
------------------------

## 作業

  coin_imgs の画像を手作業で分類して manual_classified_coin_imgs に格納します。

## ディレクトリ

- manual_classified_coin_imgs/head

  コイン画像のうち表面にあたる画像を手作業でここに格納します。

- manual_classified_coin_imgs/tail

  コイン画像のうち裏面にあたる画像を手作業でここに格納します。

- manual_classified_coin_imgs/other

  コイン画像のうち表でも裏でもない画像を手作業でここに格納します。

訓練用データの作成
------------------

## 作業

- manual_classified_coin_imgs_to_data.py

  manual_classified_coin_imgs のコイン画像を、
  1 割を検証用に、残りを訓練用に、data にコピーします。

  実行

      python3 manual_classified_coin_imgs_to_data.py


## ディレクトリ

- data

  manual_classified_coin_imgs_to_data.py がコイン画像を格納します。

訓練
----

## 作業

- train.py

  data のコイン画像で訓練します。

  実行

      python3 train.py

## ファイル

- train_weights.h5

  訓練完了後、訓練済みのモデルの重みをこのファイルに保存します。

テスト用画像の格納
------------------

## 作業

  訓練に使用した画像とは別に、新たに収集した画像を、test_orig_imgs に手作業でコピーします。

## ディレクトリ

- test_orig_imgs

テスト用コイン画像の抽出
------------------------

## 作業

- make_coin_imgs.py

  test_orig_imgs の画像から、コイン画像のみ抽出し、test_coin_imgs に格納します。

  実行

      python3 make_coin_imgs.py -t

## ディレクトリ

- test_coin_imgs

  make_coin_imgs.py が抽出したコイン画像を格納します。

コイン画像分類のテスト
----------------------

## 作業

- test_classified_coin_imgs.py

  test_coin_imgs のコイン画像を分類し、test_classified_coin_imgs に格納します。

  実行

      python3 test_classified_coin_imgs.py

## ディレクトリ

- test_classified_coin_imgs

  test_classified_coin_imgs.py が分類したコイン画像を格納します。

コイン画像分類のテスト(1枚ずつ)
-------------------------------

## 作業

- predict.py

  指定したコイン画像のテスト結果を出力します。

  実行

      python3 predict.py -f コイン画像ファイルのパス

コイン投げと判定
----------------

## 作業

- predict_uploader.py

  画像を収集するマシンで実行します。
  raspberry_pi/toss_and_capture.py から送られてきた画像を predict_upload_files に、
  画像から抽出したコイン画像を predict_coin_imgs に、それぞれ格納し、
  画像と判定結果を表示します。

  設定

    - host='0.0.0.0' および port=8080 を適宜変更します。

  実行

      python3 predict_uploader.py

- raspberry_pi/toss_and_capture.py

  Raspberry Pi で実行します。
  手動でコイン投げを行い、撮影した画像を predict_uploader.py に送ります。

  設定

    - UPLOAD_URL を predict_uploader.py を実行するマシンにあわせて修正します。

  実行

      python3 toss_and_capture.py -m

  コイン投げ器のタクトスイッチを押すとコイン投げを行います。

  ※タクトスイッチの状態を一定時間毎に参照する実装のため、
  ちょっと押しただけでは動作しないことがあります。
  動作するまで押しっぱなしにし、コイン投げが始まったら手を放します。
  再度コイン投げをする場合は、またタクトスイッチを押します。

## ディレクトリ

- predict_upload_files

  predict_uploader.py で受信した画像を格納します。

- predict_coin_imgs

  predict_uploader.py で受信した画像から抽出したコイン画像を格納します。

