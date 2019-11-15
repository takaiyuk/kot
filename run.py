import argparse
from datetime import datetime

from py.crawler import Crawler
from py.scraper import Scraper
from py.notifyer import notify


def console():
    src = Crawler().get_source()
    dct = Scraper().raw_data(src)
    print(
        """
    残り{work_count_remain}営業日: ({work_count}/{monthly_work_count} 日)

    あと{work_hour_remain:.2f}h必要: ({work_hour}/{monthly_work_hour}h)

    貯金: {saveing_time:.2f}h

    貯金を元に残り営業日の必要勤務時間数を算出すると: {work_hour_remain_by_day:.2f}h

    {today:%Y-%m-%d}の出勤・定時
        出勤: {start_time}
        定時: {teiji_time}
    """.format(
            today=datetime.today(), **dct
        )
    )


def notify_to_slack():
    try:
        page_source = Crawler().get_source()
        messages = Scraper().run(page_source)
        dt_now = datetime.now()
        title = f"{dt_now.year}/{dt_now.month}/{dt_now.day}"
        notify(title, "\n".join(messages))
    except Exception as e:
        # 打刻ない時に要素を取得できずエラー発生する
        notify("error",f"error occurred: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=notify_to_slack)

    sub = parser.add_subparsers()
    _console = sub.add_parser("console")
    _console.set_defaults(func=console)

    params = parser.parse_args()
    params.func()
