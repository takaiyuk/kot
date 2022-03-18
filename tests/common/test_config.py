import os
from dataclasses import dataclass
from typing import Any

from kot.common.config import (
    Account,
    Config,
    MyRecorder,
    ScrapeKOT,
    Slack,
    generate_config,
    load_config,
)

tmp_config_filepath = "tmp.yaml"


def create_tmp_config_filepath():
    config_string = """
account:
  id: id
  password: password
scrapekot:
  slack:
    webhook_url: scrapekot_url
    channel: scrapekot_channel
    icon_emoji: scrapekot_emoji
    username: scrapekot_username
myrecorder:
  slack:
    webhook_url: myrecorder_url
    channel: myrecorder_channel
    icon_emoji: myrecorder_emoji
    username: myrecorder_username
"""
    with open(tmp_config_filepath, "w") as f:
        f.write(config_string)


def remove_tmp_config_filepath():
    os.remove(tmp_config_filepath)


def test_load_config():
    @dataclass
    class Fixture:
        desc: str
        input: str
        expected: Config

    create_tmp_config_filepath()
    try:
        cfg = Config(
            account=Account(id="id", password="password"),
            scrapekot=ScrapeKOT(
                slack=Slack(
                    webhook_url="scrapekot_url",
                    channel="scrapekot_channel",
                    icon_emoji="scrapekot_emoji",
                    username="scrapekot_username",
                ),
            ),
            myrecorder=MyRecorder(
                slack=Slack(
                    webhook_url="myrecorder_url",
                    channel="myrecorder_channel",
                    icon_emoji="myrecorder_emoji",
                    username="myrecorder_username",
                ),
            ),
        )
        fixtures = [Fixture("tmp/tmp.yaml", tmp_config_filepath, cfg)]
        for fixture in fixtures:
            assert load_config(fixture.input) == fixture.expected, f"{fixture.desc}"
    finally:
        remove_tmp_config_filepath()


def test_generate_config():
    @dataclass
    class Fixture:
        desc: str
        input: dict[str, Any]
        expected: Config

    d = {
        "account": {"id": "id", "password": "password"},
        "scrapekot": {
            "slack": {
                "webhook_url": "scrapekot_url",
                "channel": "scrapekot_channel",
                "icon_emoji": "scrapekot_emoji",
                "username": "scrapekot_username",
            }
        },
        "myrecorder": {
            "slack": {
                "webhook_url": "myrecorder_url",
                "channel": "myrecorder_channel",
                "icon_emoji": "myrecorder_emoji",
                "username": "myrecorder_username",
            }
        },
    }
    cfg = Config(
        account=Account(id="id", password="password"),
        scrapekot=ScrapeKOT(
            slack=Slack(
                webhook_url="scrapekot_url",
                channel="scrapekot_channel",
                icon_emoji="scrapekot_emoji",
                username="scrapekot_username",
            ),
        ),
        myrecorder=MyRecorder(
            slack=Slack(
                webhook_url="myrecorder_url",
                channel="myrecorder_channel",
                icon_emoji="myrecorder_emoji",
                username="myrecorder_username",
            ),
        ),
    )
    fixtures = [Fixture("", d, cfg)]
    for fixture in fixtures:
        assert generate_config(fixture.input) == fixture.expected, f"{fixture.desc}"
