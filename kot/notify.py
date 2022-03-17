import json
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

import requests

from kot.aggregate import AggregatedData
from kot.config import Config
from kot.logger import logger


class Color(Enum):
    GREEN = "#3cb371"
    YELLOW = "#ffd700"
    RED = "#ff0000"


@dataclass
class NotifyData:
    title: str
    message: str
    color: str


class SlackClient:
    def notify(self, cfg: Config, aggregated_data: AggregatedData) -> None:
        dt_now = datetime.now()
        title = self._get_title(dt_now)
        color = self._get_color(aggregated_data.saving_time)
        message = self._get_message(aggregated_data)
        notify_data = NotifyData(title=title, message=message, color=color)
        raise ValueError  # FIXME: 開発中に誤ってSlackに投稿されてしまわないように例外を発生させている
        self._post_slack(cfg, notify_data)

    def _get_title(self, dt_now: datetime) -> str:
        title = f"{dt_now.year}/{dt_now.month}/{dt_now.day}"
        return title

    def _get_color(self, saving_time: float) -> str:
        if saving_time >= 1:
            return Color.GREEN.value
        elif saving_time >= 0:
            return Color.YELLOW.value
        else:
            return Color.RED.value

    def _get_message(self, aggregated_data: AggregatedData) -> str:
        messages = [
            f":shigyou:\t{aggregated_data.start_time}",
            f":teiji:\t{aggregated_data.teiji_time}",
            f":bank:\t{aggregated_data.saving_time}",
        ]
        message = "\n".join(messages)
        return message

    def _post_slack(self, cfg: Config, notify_data: NotifyData) -> None:
        requests.post(
            cfg.scrapekot.slack.webhook_url,
            data=json.dumps(
                {
                    "channel": cfg.scrapekot.slack.channel,
                    "attachments": [
                        {
                            "pretext": notify_data.title,
                            "color": notify_data.color,
                            "text": notify_data.message,
                        }
                    ],
                }
            ),
        )


class Console:
    @staticmethod
    def display(aggregated_data: AggregatedData, dt_today: datetime) -> None:
        kwargs = {
            "work_counts_remain": aggregated_data.work_counts_remain,
            "work_counts": aggregated_data.work_counts,
            "monthly_work_counts": aggregated_data.monthly_work_counts,
            "work_hours_remain": aggregated_data.work_hours_remain,
            "work_hours": aggregated_data.work_hours,
            "monthly_work_hours": aggregated_data.monthly_work_hours,
            "saving_time": aggregated_data.saving_time,
            "work_hours_remain_by_day": aggregated_data.work_hours_remain_by_day,
            "start_time": aggregated_data.start_time,
            "teiji_time": aggregated_data.teiji_time,
        }
        logger.info(
            """
    残り{work_counts_remain}営業日: ({work_counts}/{monthly_work_counts} 日)

    あと{work_hours_remain}必要: ({work_hours}/{monthly_work_hours})

    貯金: {saving_time}

    貯金を元に残り営業日の必要勤務時間数を算出すると: {work_hours_remain_by_day}

    {today:%Y-%m-%d}の出勤・定時
        出勤: {start_time}
        定時: {teiji_time}
""".format(
                today=dt_today, **kwargs
            )
        )
