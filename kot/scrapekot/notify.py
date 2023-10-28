from collections import OrderedDict
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Optional

from kot.common.logger import logger
from kot.common.notify import BaseSlackClient, NotifyData
from kot.scrapekot.aggregate import AggregatedData


@dataclass
class SlackClientParams:
    slack_webhook_url: str
    slack_channels: list[str]
    slack_icon_emoji: str
    slack_username: str
    dt_now: datetime


class Color(Enum):
    GREEN = "#3cb371"
    YELLOW = "#ffd700"
    RED = "#ff0000"


class SlackClient(BaseSlackClient):
    def _build_noitfy_data(self, params: SlackClientParams, data: AggregatedData) -> Optional[NotifyData]:
        message = self._get_message(data)
        title = self._get_title(params.dt_now)
        color = self._get_color(data.saving_time)
        return NotifyData(
            slack_webhook_url=params.slack_webhook_url,
            slack_channels=params.slack_channels,
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
            f":bank:\t{format_hours(aggregated_data.saving_time)}",
        ]
        message = "\n".join(messages)
        return message

    def _get_title(self, dt_now: datetime) -> str:
        title = f"{dt_now.year}/{dt_now.month}/{dt_now.day}"
        return title

    def _get_color(self, saving_time: float) -> str:
        match saving_time:
            case t if t >= 1:
                return Color.GREEN.value
            case t if t >= 0:
                return Color.YELLOW.value
            case _:
                # Avoid mypy error when using match guard: https://github.com/python/mypy/issues/14704
                pass
        return Color.RED.value

    def _slack_url(self, notify_data: NotifyData) -> str:
        return notify_data.slack_webhook_url

    def _slack_data(self, notify_data: NotifyData) -> list[dict[str, Any]]:
        data = []
        for slack_channel in notify_data.slack_channels:
            data.append(
                {
                    "username": notify_data.slack_username,
                    "icon_emoji": notify_data.slack_icon_emoji,
                    "channel": slack_channel,
                    "attachments": [
                        {
                            "pretext": notify_data.title,
                            "color": notify_data.color,
                            "text": notify_data.message,
                        }
                    ],
                }
            )
        return data


class Console:
    @staticmethod
    def display(aggregated_data: AggregatedData, dt_today: datetime, stdout: bool = True) -> str:
        kwargs = {
            "work_counts_remain": aggregated_data.work_counts_remain,
            "work_counts": aggregated_data.work_counts,
            "monthly_work_counts": aggregated_data.monthly_work_counts,
            "work_hours_remain": format_hours(aggregated_data.work_hours_remain),
            "work_hours": format_hours(aggregated_data.work_hours),
            "monthly_work_hours": int(aggregated_data.monthly_work_hours),
            "saving_time": format_hours(aggregated_data.saving_time),
            "work_hours_remain_by_day": format_hours(aggregated_data.work_hours_remain_by_day),
            "start_time": aggregated_data.start_time,
            "teiji_time": aggregated_data.teiji_time,
        }
        message = """
    残り{work_counts_remain}営業日: ({work_counts}/{monthly_work_counts} 日)

    あと{work_hours_remain}必要: ({work_hours}/{monthly_work_hours}時間)

    貯金: {saving_time}

    貯金を元に残り営業日の必要勤務時間数を算出すると: {work_hours_remain_by_day}

    {today:%Y-%m-%d}の出勤・定時
        出勤: {start_time}
        定時: {teiji_time}
""".format(
            today=dt_today, **kwargs
        )
        if stdout:
            logger.info(message)
        return message


def format_hours(hours: float) -> str:
    """
    1.05 -> 1時間05分
    1.5 -> 1時間50分
    1.50 -> 1時間50分
    0 -> 0時間00分
    """
    if hours == 0:
        return "0時間00分"
    hour_str = str(hours).split(".")[0]
    minute_str = str(hours).split(".")[1]
    # hours=2.5 を `2時間5分` ではなく `2時間50分` に変換するための対応
    if len(minute_str) == 1:
        minute_str += "0"
    return f"{hour_str}時間{minute_str}分"


def message_to_dict(message: str) -> OrderedDict[str, str]:
    od = OrderedDict()
    for m in message.replace(" ", "").split("\n"):
        if len(m) == 0:
            continue
        m_split = m.split(":")
        if len(m_split) == 1:
            continue
        key = m_split[0]
        value = ":".join(m_split[1:])
        od.update({key: value})
    return od
