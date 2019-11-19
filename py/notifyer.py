"""
scraper.py の結果を Slack に通知する君
"""
import json
import requests

from config import NOTIFY_CHANNEL, WEBHOOK_URL


def notify(title, message):
    requests.post(
        WEBHOOK_URL,
        data=json.dumps(
            {
                "channel": NOTIFY_CHANNEL,
                "attachments": [
                    {"pretext": title, "color": "#3cb371", "text": message}
                ],
            }
        ),
    )
