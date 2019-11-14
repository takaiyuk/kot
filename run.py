import datetime

from py.crawler import Crawler
from py.scraper import Scraper
from py.notifyer import notify


def main():
    try:
        page_source = Crawler().get_source()
        messages = Scraper().run(page_source)
        dt_now = datetime.datetime.now()
        notify(f"{dt_now.year}/{dt_now.month}/{dt_now.day}")
        for message in messages:
            notify(message)
    except Exception as e:
        # 打刻ない時に要素を取得できずエラー発生する
        notify(f"error occurred: {e}")


if __name__ == "__main__":
    main()
