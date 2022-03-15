# kot

## TOC

* [TOC](#TOC)
* [What is this?](#what-is-this?)
* [Scrape KOT](#scrape-kot)
    * [Run with Docker](#run-with-docker)
    * [Run on AWS Lambda](#run-on-aws-lambda)
* [My Recorder](#my-recorder)
* [Typer Help](#typer-help)
* [How to install docker (macOS)](#how-to-install-docker-macos)

## What is this?

Selenium を利用して以下の2機能を実現している

- King of Time の勤怠データから勤務時間の貯金時間等を計算する
- My Recorder で打刻する

## Scrape KOT

### Run with Docker

事前に Docker を起動し、サインインしておく

Docker がインストールされてない場合は、[こちら](https://github.com/takaiyuk/kot#how-to-install-docker)を参照

```
$ git clone https://github.com/takaiyuk/kot.git
$ cd kot
$ mkdir ~/.kot
$ cp config.yaml.example ~/.kot/config.yaml
$ ./scripts/docker/kot/pull.sh
$ ./scripts/scrapekot.sh notify
```

出力イメージ

![Slack Notify Image](https://github.com/takaiyuk/kot/blob/master/docs/source/_static/img/notify-green.png)

<br>

Slack チャンネルに通知させたくない場合は `console` をつけて実行することで自身のコンソール上のみに出力させることも可能

```
$ ./scripts/scrapekot.sh console
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

### Run on AWS Lambda

AWS Lambda で動かすためにコンテナイメージを利用して Lambda 関数コードをデプロイすることができる（ref. [コンテナイメージで Python Lambda 関数をデプロイする](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-image.html)）

```
$ cp scripts/docker/lambda/.env.example scripts/docker/lambda/.env
$ ./scripts/docker/lambda/build.sh
$ ./scripts/docker/lambda/push.sh
```

**上記のコンテナイメージには `config.yaml` 等重要な情報を含むためアップロードするアカウントに注意する**

<br>

## My Recorder

```
$ ./scripts/myrecorder.sh ${CMD}
```

${CMD} は以下の通り

- `start`: 出勤
- `end`: 退勤
- `rest_start`: 休憩開始
- `rest_end`: 休憩終了

<br>

## Typer Help

`Typer` ヘルプ

```
$ python -m kot --help
Usage: python -m kot [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  myrecorder
  scrape
```

```
$ python -m kot scrape --help
Usage: python -m kot scrape [OPTIONS]

Options:
  --amazon-linux / --no-amazon-linux
                                  [default: no-amazon-linux]
  --chrome / --no-chrome          [default: chrome]
  --chronium / --no-chronium      [default: no-chronium]
  --firefox / --no-firefox        [default: no-firefox]
  --headless / --no-headless      [default: headless]
  --console / --no-console        [default: console]
  --help                          Show this message and exit.
```

```
$ python -m kot myrecorder --help
Usage: python -m kot myrecorder [OPTIONS] COMMAND

Arguments:
  COMMAND  [required]

Options:
  --yes / --no-yes                [default: no-yes]
  --message TEXT
  --debug / --no-debug            [default: debug]
  --amazon-linux / --no-amazon-linux
                                  [default: no-amazon-linux]
  --chrome / --no-chrome          [default: chrome]
  --chronium / --no-chronium      [default: no-chronium]
  --firefox / --no-firefox        [default: no-firefox]
  --headless / --no-headless      [default: headless]
  --help                          Show this message and exit.
```

## How to install docker (macOS)

（不明な場合は[こちらの記事](https://qiita.com/kurkuru/items/127fa99ef5b2f0288b81#docker-for-mac%E3%82%92%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB-package)等を参考にする）

1. [Docker for Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac) をダウンロードする（ダウンロードにはアカウント作成が必要）
2. ダウンロード・インストールが完了したら、Docker for Mac を起動する
3. ステータスバーにクジラのアイコンが出るので、先程作成した Docker の ID/Password でサインインする
