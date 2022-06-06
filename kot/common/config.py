import os
from dataclasses import dataclass
from typing import Any

import yaml

IS_AWS_LAMBDA_RUNTIME: bool = os.getenv("AWS_LAMBDA_FUNCTION_NAME") is not None


@dataclass
class Account:
    id: str
    password: str


@dataclass
class Slack:
    webhook_url: str
    channel: str
    icon_emoji: str
    username: str


@dataclass
class ScrapeKOT:
    slack: Slack


@dataclass
class MyRecorder:
    slack: Slack


@dataclass
class Config:
    """
    account:
        id: id
        password: passaword
    scrapekot:
        slack:
            webhook_url: url
            channel: channel
            icon_emoji: icon
            username: username
    myrecorder:
        slack:
            webhook_url: url
            channel: channel
            icon_emoji: icon
            username: username
    """

    account: Account
    scrapekot: ScrapeKOT
    myrecorder: MyRecorder


def load_config(filepath: str) -> Config:
    if IS_AWS_LAMBDA_RUNTIME:
        d = read_lambda_env()
    else:
        d = read_env(filepath)
    cfg = generate_config(d)
    return cfg


def read_env(filepath: str) -> dict[str, Any]:
    with open(filepath, "r") as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def generate_config(d: dict[str, Any]) -> Config:
    return Config(
        account=Account(
            id=d["account"]["id"],
            password=d["account"]["password"],
        ),
        scrapekot=ScrapeKOT(
            slack=Slack(
                webhook_url=d["scrapekot"]["slack"].get("webhook_url", ""),
                channel=d["scrapekot"]["slack"].get("channel", ""),
                icon_emoji=d["scrapekot"]["slack"].get("icon_emoji", ""),
                username=d["scrapekot"]["slack"].get("username", ""),
            ),
        ),
        myrecorder=MyRecorder(
            slack=Slack(
                webhook_url=d["myrecorder"]["slack"].get("webhook_url", ""),
                channel=d["myrecorder"]["slack"].get("channel", ""),
                icon_emoji=d["myrecorder"]["slack"].get("icon_emoji", ""),
                username=d["myrecorder"]["slack"].get("username", ""),
            ),
        ),
    )


def read_lambda_env() -> dict[str, Any]:
    d = {
        "account": {
            "id": os.environ["ACCOUNT_ID"],
            "password": os.environ["ACCOUNT_PAWSSWORD"],
        },
        "myrecorder": {
            "slack": {
                "webhook_url": os.environ["SLACK_WEBHOOK_URL"],
                "channel": os.environ["SLACK_CHANNEL"],
                "icon_emoji": os.environ["SLACK_ICON_EMOJI"],
                "username": os.environ["SLACK_USERNAME"],
            }
        },
        "scrapekot": {
            "slack": {
                "webhook_url": "",
                "channel": "",
                "icon_emoji": "",
                "username": "",
            }
        },
    }
    return d
