"""
scraper.py の結果を Slack に通知する君
"""
import subprocess

from config import SLACK_WEB_API_TOKEN, NOTIFY_CHANNEL


def notify(message):
    cmd = f"curl https://slack.com/api/chat.postMessage?token={SLACK_WEB_API_TOKEN}&channel={NOTIFY_CHANNEL}&text={message}"
    subprocess.call(cmd.split())
