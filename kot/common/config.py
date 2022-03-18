from dataclasses import dataclass
from typing import Any

import yaml


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
    with open(filepath, "r") as f:
        d = yaml.load(f, Loader=yaml.FullLoader)
    cfg = generate_config(d)
    return cfg


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
