from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any

from kot.common.logger import logger
from kot.common.notify import BaseSlackClient, NotifyData
from kot.scrapekot.aggregate import AggregatedData


@dataclass
class SlackClientParams:
    slack_webhook_url: str
    slack_channel: str
    slack_icon_emoji: str
    slack_username: str
    dt_now: datetime


class Color(Enum):
    GREEN = "#3cb371"
    YELLOW = "#ffd700"
    RED = "#ff0000"


class SlackClient(BaseSlackClient):
    def _build_noitfy_data(
        self, params: SlackClientParams, data: AggregatedData
    ) -> NotifyData:
        message = self._get_message(data)
        title = self._get_title(params.dt_now)
        color = self._get_color(data.saving_time)
        return NotifyData(
            slack_webhook_url=params.slack_webhook_url,
            slack_channel=params.slack_channel,
            slack_icon_emoji=params.slack_icon_emoji,
            slack_username=params.slack_username,
            message=message,
            title=title,
            color=color,
        )

    def _get_message(self, aggregated_data: AggregatedData) -> str:
        messages = [
            f":shigyou:\t{aggregated_data.start_time}",
            f":teiji:\t{aggregated_data.teiji_time}",
            f":bank:\t{aggregated_data.saving_time}",
        ]
        message = "\n".join(messages)
        return message

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

    def _slack_url(self, notify_data: NotifyData) -> str:
        return notify_data.slack_webhook_url

    def _slack_data(self, notify_data: NotifyData) -> dict[str, Any]:
        return {
            "channel": notify_data.slack_channel,
            "attachments": [
                {
                    "pretext": notify_data.title,
                    "color": notify_data.color,
                    "text": notify_data.message,
                }
            ],
        }


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
