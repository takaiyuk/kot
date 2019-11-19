# scrape-king-of-time

## What is This?

King of Time をスクレイピングして、 勤務時間の貯金等を計算＆通知してくれる君

## How to Use?

### Run with Docker

事前に Docker を起動し、サインインしておく

Docker がインストールされてない場合は、[こちら](https://github.com/takaiyuk/scrape-king-of-time#how-to-install-docker)を参照

```
git clone https://github.com/takaiyuk/scrape-king-of-time.git
cd scrape-king-of-time
cp config.py.example config.py  # config.py に自分の King of Time の ID/PW 等を入力する
docker run -v "${PWD}":/scrape_kot -v "${PWD}":/scrape_kot/drivers -it --rm takaiyuk/scrape-kot run.py
```

- Output example

![Slack Notify Image](https://github.com/takaiyuk/scrape-king-of-time/blob/master/docs/source/_static/img/slack-notify-message-image.png)

<br>

If you do not want to notify on slack channel, you can make the result output only on your console with `console` command:

```
docker run -v "${PWD}":/scrape_kot -v "${PWD}":/scrape_kot/drivers -it --rm takaiyuk/scrape-kot run.py console
```

- Output example

```
    残り12営業日: (8/20 日)

    あと94.34h必要: (65.26/160h)

    貯金: 1.26h

    貯金を元に残り営業日の必要勤務時間数を算出すると: 7.52h

    2019-11-14の出勤・定時
        出勤: 10:15
        定時: 19:15
```

<br>

### Run on Local

You can run without docker. Python 3.6 or later are required.

```
git clone https://github.com/takaiyuk/scrape-king-of-time.git
cd scrape-king-of-time
python py/utils/download_chromedriver.py --os=mac # or --os=linux. default is --os=mac.
pip install -r requirements.txt
cp config.py.example config.py  # config.py に自分の King of Time の ID/PW 等を入力する
python run.py  # slack に 通知させたくない場合は `python run.py console`
```

<br>

### Run on AWS Lambda

Prepare lambda deploy package with docker

```
python py/utils/lambda_prepare.py
rsync -ar ./* ./deploy_package --exclude 'deploy_package' --exclude 'drivers/chromedriver'
cd deploy_package
docker build -t scrape-king-of-time .
docker run -v "${PWD}":/var/task -it --rm scrape-king-of-time
```

Place the created `deploy_package.zip` on S3 and set the Lambda function appropriately.

**Note: MAKE SURE to use your PRIVATE S3 accoount because `deploy_package.zip` includes very important information (ID and password for king-of-time).**

<br>

## How to install docker

[Docker for Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac) をダウンロードする。ダウンロードするためにはアカウント作成が必要です。（不明な場合は[こちらの記事](https://qiita.com/kurkuru/items/127fa99ef5b2f0288b81#docker-for-mac%E3%82%92%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB-package)を参考に Docker for Mac をダウンロードしてください）

ダウンロード・インストールが完了したら、Docker for Mac を起動してください。
ステータスバーにクジラのアイコンが出るので、先程作成した Docker の ID/Password でサインインしてください。
