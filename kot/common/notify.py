import json
from dataclasses import dataclass
from typing import Any, Optional

import requests


@dataclass
class NotifyData:
    slack_webhook_url: str
    slack_channels: list[str]
    slack_icon_emoji: str
    slack_username: str
    message: str
    title: Optional[str] = None
    color: Optional[str] = None


class BaseSlackClient:
    def notify(self, params: Any, data: Any = None) -> None:
        notify_data = self._build_noitfy_data(params, data)
        if notify_data is None:
            pass
        else:
            self._post_slack(notify_data)

    def _build_noitfy_data(self, params: Any, data: Any) -> Optional[NotifyData]:
        raise NotImplementedError

    def _post_slack(self, notify_data: NotifyData) -> None:
        url = self._slack_url(notify_data)
        data = self._slack_data(notify_data)
        for d in data:
            requests.post(url, json.dumps(d))

    def _slack_url(self, notify_data: NotifyData) -> str:
        raise NotImplementedError

    def _slack_data(self, notify_data: NotifyData) -> list[dict[str, Any]]:
        raise NotImplementedError
