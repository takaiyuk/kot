# kot

## TOC

- [TOC](#TOC)
- [概要](#概要)
- [実行環境の準備](#実行環境の準備)
- [Scrape KOT](#scrape-kot)
  - [Slack に通知](#slack-に通知)
  - [Console に通知](#console-に通知)
  - [AWS Lambda で実行](#aws-lambda-で実行)
- [My Recorder](#my-recorder)
- [Development](#development)
  - [Typer Help](#typer-help)
  - [Lint](#lint)
    - [type check](#type-check)
    - [test](#test)
  - [Pydeps](#pydeps)

## 概要

以下の機能が CLI で操作できる

- KING OF TIME の勤怠データから勤務時間の貯金時間等を計算する
- My レコーダーで打刻する

## 実行環境の準備

### Docker で実行

```shell
$ git clone https://github.com/takaiyuk/kot.git
$ cd kot
$ mkdir ~/.kot
# config.yaml を適宜書き換える
$ cp ./config.yaml.example ~/.kot/config.yaml
$ ./scripts/docker/kot/pull.sh
```

### ローカルで実行

```shell
$ git clone https://github.com/takaiyuk/kot.git
$ cd kot
# config.yaml を適宜書き換える
$ cp ./config.yaml.example ./config.yaml
$ pip install -r requirements.txt
```

## Scrape KOT

### Slack に通知

#### Docker で実行

```shell
$ ./scripts/scrapekot.sh slack
```

#### ローカルで実行

```shell
$ python -m kot scrape --no-console
```

#### 出力イメージ

![Slack Notify Image](https://github.com/takaiyuk/kot/blob/master/statics/img/notify-green.png)

### Console に通知

Slack チャンネルに通知させたくない場合は `console` をつけて実行することで自身のコンソール上のみに出力させることも可能

#### Docker で実行

```shell
$ ./scripts/scrapekot.sh console
```

#### ローカルで実行

```shell
$ python -m kot scrape --console
```

#### 出力イメージ

```
    残り12営業日: (8.0/20.0 日)

    あと94時間34分必要: (65時間26分/160時間)

    貯金: 1時間26分

    貯金を元に残り営業日の必要勤務時間数を算出すると: 7時間52分

    2019-11-14の出勤・定時
        出勤: 10:15
        定時: 19:15
```

### AWS Lambda で実行

AWS Lambda で動かすためにコンテナイメージを利用して Lambda 関数コードをデプロイすることができる（ref. [コンテナイメージで Python Lambda 関数をデプロイする](https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-image.html)）

```shell
# config.yaml を適宜書き換える
$ cp scripts/docker/lambda/.env.example scripts/docker/lambda/.env
$ ./scripts/docker/lambda/build.sh
$ ./scripts/docker/lambda/push.sh
```

**上記のコンテナイメージには `config.yaml` 等重要な情報を含むためアップロードするアカウントに注意する**

## My Recorder

利用可能な `${CMD}` は以下の通り

- `start`: 出勤
- `end`: 退勤
- `rest_start`: 休憩開始
- `rest_end`: 休憩終了

### Docker で実行

```shell
$ ./scripts/myrecorder.sh ${CMD}
```

Slack に特定のメッセージを通知する場合には以下のようにする

```shell
$ ./scripts/myrecorder.sh ${CMD} "Some messages"
```

### ローカルで実行

```shell
$ python -m kot myrecorder ${CMD}
```

Slack に特定のメッセージを通知する場合には以下のようにする

```shell
$ python -m kot myrecorder ${CMD} --message "Some messages"
```

## Development

### Typer Help

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
  --debug / --no-debug            [default: no-debug]
  --amazon-linux / --no-amazon-linux
                                  [default: no-amazon-linux]
  --chrome / --no-chrome          [default: chrome]
  --chronium / --no-chronium      [default: no-chronium]
  --firefox / --no-firefox        [default: no-firefox]
  --headless / --no-headless      [default: headless]
  --help                          Show this message and exit.
```

### Lint

#### type check

```shell
$ make mypy
```

#### test

```shell
$ make test
```

### Pydeps

```shell
$ make pydeps
```

![kot.svg](https://github.com/takaiyuk/kot/blob/master/statics/img/kot.svg)
