import json
from dataclasses import dataclass
from typing import Any

from kot.myrecorder.notify import NotifyData, SlackClient, SlackClientParams

api = SlackClient()


def test_SlackClient_notify():
    pass


def test_SlackClient__build_noitfy_data(mocker):
    @dataclass
    class Fixture:
        desc: str
        params: SlackClientParams
        expected: NotifyData

    mocker.patch("random.randint", return_value=0)

    # params.yes にかかわらず params.is_debug=False and params.is_punched=True のときのみ notify_data が返却される
    yes_debug_punch_tuple = [
        (True, False, True),
        (True, False, False),
        (True, True, True),
        (True, True, False),
        (False, False, True),
        (False, False, False),
        (False, True, True),
        (False, True, False),
    ]
    params = [
        SlackClientParams(
            slack_webhook_url="myrecorder_url",
            slack_channel="myrecorder_channel",
            slack_icon_emoji="myrecorder_emoji",
            slack_username="myrecorder_username",
            command="start",
            message="",
            yes=yes,
            is_debug=is_debug,
            is_punched=is_punched,
        )
        for yes, is_debug, is_punched in yes_debug_punch_tuple
    ]
    expected = [
        NotifyData(
            slack_webhook_url="myrecorder_url",
            slack_channel="myrecorder_channel",
            slack_icon_emoji="myrecorder_emoji",
            slack_username="myrecorder_username",
            message=":shukkin:",
        ),
        None,
        None,
        None,
        NotifyData(
            slack_webhook_url="myrecorder_url",
            slack_channel="myrecorder_channel",
            slack_icon_emoji="myrecorder_emoji",
            slack_username="myrecorder_username",
            message=":shukkin:",
        ),
        None,
        None,
        None,
    ]
    fixtures = [Fixture("", p, e) for p, e in zip(params, expected)]
    for fixture in fixtures:
        assert api._build_noitfy_data(fixture.params) == fixture.expected, fixture.desc


def test_SlackClient__post_slack(mocker):
    @dataclass
    class Fixture:
        desc: str
        notify_data: NotifyData

    def mock_func_requests_post(url, data):
        assert url == "myrecorder_url"
        assert data == json.dumps(
            {
                "username": "myrecorder_username",
                "icon_emoji": "myrecorder_emoji",
                "channel": "myrecorder_channel",
                "text": "test_message",
            }
        )

    mocker.patch("requests.post", side_effect=mock_func_requests_post)
    notify_data = NotifyData(
        slack_webhook_url="myrecorder_url",
        slack_channel="myrecorder_channel",
        slack_icon_emoji="myrecorder_emoji",
        slack_username="myrecorder_username",
        message="test_message",
    )
    fixtures = [Fixture("", notify_data)]
    for fixture in fixtures:
        api._post_slack(fixture.notify_data)


def test_SlackClient__slack_url():
    @dataclass
    class Fixture:
        desc: str
        notify_data: NotifyData
        expected: str

    notify_data = NotifyData(
        slack_webhook_url="myrecorder_url",
        slack_channel="myrecorder_channel",
        slack_icon_emoji="myrecorder_emoji",
        slack_username="myrecorder_username",
        message="test_message",
        title="test_title",
        color="green",
    )
    fixtures = [Fixture("", notify_data, "myrecorder_url")]
    for fixture in fixtures:
        assert api._slack_url(fixture.notify_data) == fixture.expected, fixture.desc


def test_SlackClient__slack_data():
    @dataclass
    class Fixture:
        desc: str
        notify_data: NotifyData
        expected: dict[str, Any]

    notify_data = NotifyData(
        slack_webhook_url="myrecorder_url",
        slack_channel="myrecorder_channel",
        slack_icon_emoji="myrecorder_emoji",
        slack_username="myrecorder_username",
        message="test_message",
    )
    expected = {
        "username": "myrecorder_username",
        "icon_emoji": "myrecorder_emoji",
        "channel": "myrecorder_channel",
        "text": "test_message",
    }
    fixtures = [Fixture("", notify_data, expected)]
    for fixture in fixtures:
        assert api._slack_data(fixture.notify_data) == fixture.expected, fixture.desc
