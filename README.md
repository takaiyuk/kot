# scrape-king-of-time

## What is This?

King of Time をスクレイピングして、 勤務時間の貯金等を計算＆通知してくれる君

## How to Use?

```
git clone https://github.com/takaiyuk/scrape-king-of-time.git
cd scrape-king-of-time
python py/utils/download_chromedriver.py  # For Mac OS
pip install -r requirements.txt
cp config.py.example config.py  # config.py に自分の King of Time の ID/PW 等を入力する
python run.py
```

If you do not want to notify on slack channel, you can make the result output only on your console with `console` command:

```
python run.py console
```
