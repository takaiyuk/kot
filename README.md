# scrape-king-of-time

## What is This?

King of Time をスクレイピングして、 勤務時間の貯金等を計算＆通知してくれる君

## How to Use?

```
git clone https://github.com/takaiyuk/scrape-king-of-time.git
cd scrape-king-of-time
python py/utils/download_chromedriver.py --os=mac # or --os=linux. default is --os=mac.
pip install -r requirements.txt
cp config.py.example config.py  # config.py に自分の King of Time の ID/PW 等を入力する
python run.py
```

Output example

![Slack Notify Image](https://github.com/takaiyuk/scrape-king-of-time/blob/master/docs/source/_static/img/slack-notify-message-image.png)

<br>

If you do not want to notify on slack channel, you can make the result output only on your console with `console` command:

```
python run.py console
```

Output example

```
    残り12営業日: (8/20 日)

    あと94.34h必要: (65.26/160h)

    貯金: 1.26h

    貯金を元に残り営業日の必要勤務時間数を算出すると: 7.52h

    2019-11-14の出勤・定時
        出勤: 10:15
        定時: 19:15
```
