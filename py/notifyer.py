"""
scraper.py の結果を Slack に通知する君
"""
import json
import requests

from config import NOTIFY_CHANNEL, WEBHOOK_URL
from py.const import COLOR_RED, COLOR_YELLOW, COLOR_GREEN


def notify(title, message, saving_time):
    if saving_time < 0:
        color = COLOR_RED
    elif saving_time < 1:
        color = COLOR_YELLOW
    else:
        color = COLOR_GREEN
    requests.post(
        WEBHOOK_URL,
        data=json.dumps(
            {
                "channel": NOTIFY_CHANNEL,
                "attachments": [{"pretext": title, "color": color, "text": message}],
            }
        ),
    )
