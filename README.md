# scrape-king-of-time

## TOC

* [TOC](#TOC)
* [これは何か？](#これは何か)
* [使い方](#使い方)
    * [Run with Docker](#run-with-docker)
    * [Run on Local (非推奨)](#run-on-local-非推奨)
    * [Run on AWS Lambda](#run-on-aws-lambda)
* [My Recorder](#my-recorder)
* [How to install docker (macOS)](#how-to-install-docker-macos)

## これは何か？

King of Time をスクレイピングして、 勤務時間の貯金等を計算＆通知してくれる君

[My Recorder で打刻をする機能も追加](https://github.com/takaiyuk/scrape-king-of-time#my-recorder)した

## 使い方

### Run with Docker

事前に Docker を起動し、サインインしておく

Docker がインストールされてない場合は、[こちら](https://github.com/takaiyuk/scrape-king-of-time#how-to-install-docker)を参照

```
git clone https://github.com/takaiyuk/scrape-king-of-time.git
cd scrape-king-of-time
mkdir ~/.scrape_kot
cp config.py.example ~/.scrape_kot/config.py  # config.py に自分のKing of TimeのID/PW等を入力する
./shell/pull.sh
./scrapekot.sh
```

出力イメージ

![Slack Notify Image](https://github.com/takaiyuk/scrape-king-of-time/blob/master/docs/source/_static/img/notify-green.png)

<br>

Slack チャンネルに通知させたくない場合は `console` コマンドをつけて実行することで自身のコンソール上のみに出力させることも可能

```
./scrapekot.sh console
```

出力イメージ

```
    残り12営業日: (8.0/20.0 日)

    あと94時間34分必要: (65時間26分/160時間)

    貯金: 1時間26分

    貯金を元に残り営業日の必要勤務時間数を算出すると: 7時間52分

    2019-11-14の出勤・定時
        出勤: 10:15
        定時: 19:15
```

<br>

### Run on Local (非推奨)

Docker を利用せずにローカル実行もできる（Python 3.6 以降が必須）

Chromedriver のバージョンは自身の環境の Chrome と互換性のあるバージョンを指定する

```
git clone https://github.com/takaiyuk/scrape-king-of-time.git
cd scrape-king-of-time
python py/utils/download_chromedriver.py --os=mac --version=79.0.3945.36  # or --os=linux
pip install -r requirements.txt
cp config.py.example config.py  # config.py に自分のKing of TimeのID/PW等を入力する
python run.py  # slackに通知させたくない場合は `python run.py console`
```

<br>

### Run on AWS Lambda

Lambda デプロイパッケージを用意する (cf. https://qiita.com/nabehide/items/754eb7b7e9fff9a1047d)

```
./lambda_prepare.sh
cd deploy_package
./lambda_build.sh
```

実行後生成された `deploy_package.zip` を S3 に配置し、Lambda 関数を適切に設定する

**`deploy_package.zip` は重要な情報を含むためアップロードするアカウントに注意する**

<br>

## My Recorder

ブラウザから打刻できるやつ（My Recorder）で打刻をコマンドから行う

- Docker
```
./myrecorder.sh ${CMD}
```

- Python (非推奨)
```
./shell/myrecorder-py.sh ${CMD}
```

${CMD} は以下の通り

- `start`: 出勤
- `end`: 退勤
- `rest-start`: 休憩開始
- `rest-end`: 休憩終了

<br>

また `-y` オプションでプロンプトをスキップして実行可能（打刻なので注意）

- Docker
```
./myrecorder.sh ${CMD} -y
```

- Python (非推奨)
```
./shell/myrecorder-py.sh ${CMD} -y
```

また `message` オプションでSlack通知するメッセージをカスタムで追加できる（デフォルトはconst.py以下の `CMD_MESSAGE_DICT` 内のKeyに相当するリストの中からランダムに選択される）

- Docker
```
./myrecorder.sh ${CMD} -y 圧倒的出勤っ...!!
```

- Python (非推奨)
```
./shell/myrecorder-py.sh ${CMD} -y 圧倒的退勤っ...!!
```

<br>

また My Recorder で打刻時に特定のSlackチャンネルに出勤・退勤のメッセージを送信可能

`config.py` で `MYRECORDER_WEBHOOK_URL` 及び `MYRECORDER_NOTIFY_CHANNEL` を設定すれば特定のSlackチャンネルに incoming webhook で出勤・退勤のメッセージを送信することができる（未設定ならばスキップされる）

## How to install docker (macOS)

（不明な場合は[こちらの記事](https://qiita.com/kurkuru/items/127fa99ef5b2f0288b81#docker-for-mac%E3%82%92%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB-package)等を参考にする）

1. [Docker for Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac) をダウンロードする（ダウンロードにはアカウント作成が必要）
2. ダウンロード・インストールが完了したら、Docker for Mac を起動する
3. ステータスバーにクジラのアイコンが出るので、先程作成した Docker の ID/Password でサインインする
