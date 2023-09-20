import random
from dataclasses import dataclass
from typing import Any, Optional

from kot.common.logger import logger
from kot.common.notify import BaseSlackClient, NotifyData
from kot.myrecorder import MyRecorderOptions


@dataclass
class SlackClientParams:
    slack_webhook_url: str
    slack_channels: list[str]
    slack_icon_emoji: str
    slack_username: str
    command: str
    message: str
    yes: bool
    is_debug: bool
    is_punched: bool


class SlackClient(BaseSlackClient):
    def _build_noitfy_data(self, params: SlackClientParams, data: Any = None) -> Optional[NotifyData]:
        if params.message is None or params.message == "":
            kintai_messages = getattr(MyRecorderOptions, params.command).messages
            idx = random.randint(0, len(kintai_messages) - 1)
            kintai_message = kintai_messages[idx]
        else:
            kintai_message = params.message
        if not params.is_debug and params.is_punched:
            logger.info(f"通知されるメッセージ: {kintai_message}")
        else:
            logger.info(f"以下の通知はスキップされます: {kintai_message}")
            return None
        return NotifyData(
            slack_webhook_url=params.slack_webhook_url,
            slack_channels=params.slack_channels,
            slack_icon_emoji=params.slack_icon_emoji,
            slack_username=params.slack_username,
            message=kintai_message,
        )

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
                    "text": notify_data.message,
                }
            )
        return data
