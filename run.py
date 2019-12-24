import argparse
from datetime import datetime
import traceback
import sys
from typing import Any

from py.crawler import Crawler
from py.scraper import Scraper
from py.notifyer import notify


def console(params: argparse.Namespace) -> None:
    src = Crawler(params).get_source()
    dct, saving_time = Scraper(html=src).raw_data()
    print(
        """
    残り{work_count_remain}営業日: ({work_count}/{monthly_work_count} 日)

    あと{work_hours_remain}必要: ({work_hours}/{monthly_work_hours})

    貯金: {saving_time}

    貯金を元に残り営業日の必要勤務時間数を算出すると: {work_hours_remain_by_day}

    {today:%Y-%m-%d}の出勤・定時
        出勤: {start_time}
        定時: {teiji_time}
    """.format(
            today=datetime.today(), **dct
        )
    )


def notify_to_slack(params: argparse.Namespace) -> None:
    try:
        src = Crawler(params).get_source()
        messages, saving_time = Scraper(html=src).scrape()
        dt_now = datetime.now()
        title = f"{dt_now.year}/{dt_now.month}/{dt_now.day}"
        notify(title, "\n".join(messages), saving_time)
    except Exception as e:
        # 打刻ない時に要素を取得できずエラー発生する
        t, v, tb = sys.exc_info()
        x = traceback.format_exception(t, v, tb)
        notify("error", f"error occurred: {''.join(x)}", 0)
        raise e


# Function for lambda execution
def main(event: Any = None, context: Any = None) -> None:
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=notify_to_slack)

    sub = parser.add_subparsers()
    _console = sub.add_parser("console")
    _console.set_defaults(func=console)

    params = parser.parse_args()
    params.lambda_deploy = True
    params.func(params)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.set_defaults(func=notify_to_slack)

    sub = parser.add_subparsers()
    _console = sub.add_parser("console")
    _console.set_defaults(func=console)

    params = parser.parse_args()
    params.lambda_deploy = False
    params.func(params)
