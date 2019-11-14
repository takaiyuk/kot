"""
scraper.py の結果を Slack に通知する君
"""
import requests, json

from config import SLACK_WEB_API_TOKEN, NOTIFY_CHANNEL, WEBHOOK_URL

def notify(message):
  requests.post(WEBHOOK_URL, data = json.dumps({
    'channel': NOTIFY_CHANNEL,
    'text': message,
  }))
