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
    channels: list[str]
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
            channels:
              - channel_a
            icon_emoji: icon
            username: username
    myrecorder:
        slack:
            webhook_url: url
            channels:
              - channel_a
              - channel_b
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
                channels=d["scrapekot"]["slack"].get("channels", [""]),
                icon_emoji=d["scrapekot"]["slack"].get("icon_emoji", ""),
                username=d["scrapekot"]["slack"].get("username", ""),
            ),
        ),
        myrecorder=MyRecorder(
            slack=Slack(
                webhook_url=d["myrecorder"]["slack"].get("webhook_url", ""),
                channels=d["myrecorder"]["slack"].get("channels", [""]),
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
                "webhook_url": os.environ["MYRECORDER_SLACK_WEBHOOK_URL"],
                "channels": [os.environ["MYRECORDER_SLACK_CHANNEL"]],
                "icon_emoji": os.environ["MYRECORDER_SLACK_ICON_EMOJI"],
                "username": os.environ["MYRECORDER_SLACK_USERNAME"],
            }
        },
        "scrapekot": {
            "slack": {
                "webhook_url": os.environ["SCRAPEKOT_SLACK_WEBHOOK_URL"],
                "channels": [os.environ["SCRAPEKOT_SLACK_CHANNEL"]],
                "icon_emoji": os.environ["SCRAPEKOT_SLACK_ICON_EMOJI"],
                "username": os.environ["SCRAPEKOT_SLACK_USERNAME"],
            }
        },
    }
    return d
