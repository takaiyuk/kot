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
    read_env,
    read_lambda_env,
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


def test_read_env():
    @dataclass
    class Fixture:
        desc: str
        input: str
        expected: dict[str, Any]

    create_tmp_config_filepath()
    try:
        d = {
            "account": {"id": "id", "password": "password"},
            "scrapekot": {
                "slack": {
                    "webhook_url": "scrapekot_url",
                    "channel": "scrapekot_channel",
                    "icon_emoji": "scrapekot_emoji",
                    "username": "scrapekot_username",
                },
            },
            "myrecorder": {
                "slack": {
                    "webhook_url": "myrecorder_url",
                    "channel": "myrecorder_channel",
                    "icon_emoji": "myrecorder_emoji",
                    "username": "myrecorder_username",
                },
            },
        }
        fixtures = [Fixture("tmp/tmp.yaml", tmp_config_filepath, d)]
        for fixture in fixtures:
            assert read_env(fixture.input) == fixture.expected, f"{fixture.desc}"
    finally:
        remove_tmp_config_filepath()


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


def test_read_lambda_env():
    @dataclass
    class Fixture:
        desc: str
        input: dict[str, Any]
        expected: dict[str, Any]

    d = {
        "ACCOUNT_ID": "account_id",
        "ACCOUNT_PAWSSWORD": "account_password",
        "SLACK_WEBHOOK_URL": "scrapekot_url",
        "SLACK_CHANNEL": "scrapekot_channel",
        "SLACK_ICON_EMOJI": "scrapekot_emoji",
        "SLACK_USERNAME": "scrapekot_username",
    }
    expected = {
        "account": {
            "id": "account_id",
            "password": "account_password",
        },
        "myrecorder": {
            "slack": {
                "webhook_url": "scrapekot_url",
                "channel": "scrapekot_channel",
                "icon_emoji": "scrapekot_emoji",
                "username": "scrapekot_username",
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
    fixtures = [Fixture("", d, expected)]
    for fixture in fixtures:
        for k, v in fixture.input.items():
            os.environ[k] = v
        assert read_lambda_env() == fixture.expected, f"{fixture.desc}"
