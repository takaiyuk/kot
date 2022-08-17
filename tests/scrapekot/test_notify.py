import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from kot.scrapekot.aggregate import AggregatedData
from kot.scrapekot.notify import (
    Color,
    Console,
    NotifyData,
    SlackClient,
    SlackClientParams,
    format_hours,
)

api = SlackClient()


def test_SlackClient_notify():
    pass


def test_SlackClient__build_noitfy_data(mocker):
    @dataclass
    class Fixture:
        desc: str
        params: SlackClientParams
        data: AggregatedData
        expected: NotifyData

    params = SlackClientParams(
        slack_webhook_url="scrapekot_url",
        slack_channel="scrapekot_channel",
        slack_icon_emoji="scrapekot_emoji",
        slack_username="scrapekot_username",
        dt_now=datetime(2022, 3, 17, 0, 7, 37, 819883),
    )
    data = AggregatedData(
        work_counts_remain=-1,
        work_counts=-1,
        monthly_work_counts=-1,
        work_hours_remain=-1,
        work_hours=-1,
        monthly_work_hours=-1,
        saving_time=1.25,
        work_hours_remain_by_day=-1,
        start_time="09:00",
        teiji_time="18:00",
    )
    message = api._get_message(data)
    title = api._get_title(params.dt_now)
    color = api._get_color(data.saving_time)
    expected = NotifyData(
        slack_webhook_url="scrapekot_url",
        slack_channel="scrapekot_channel",
        slack_icon_emoji="scrapekot_emoji",
        slack_username="scrapekot_username",
        message=message,
        title=title,
        color=color,
    )
    fixtures = [Fixture("", params, data, expected)]
    for fixture in fixtures:
        assert (
            api._build_noitfy_data(fixture.params, fixture.data) == fixture.expected
        ), fixture.desc


def test_SlackClient__post_slack(mocker):
    @dataclass
    class Fixture:
        desc: str
        notify_data: NotifyData

    def mock_func_requests_post(url, data):
        assert url == "scrapekot_url"
        assert data == json.dumps(
            {
                "username": "scrapekot_username",
                "icon_emoji": "scrapekot_emoji",
                "channel": "scrapekot_channel",
                "attachments": [
                    {
                        "pretext": "test_title",
                        "color": "green",
                        "text": "test_message",
                    }
                ],
            }
        )

    mocker.patch("requests.post", side_effect=mock_func_requests_post)
    notify_data = NotifyData(
        slack_webhook_url="scrapekot_url",
        slack_channel="scrapekot_channel",
        slack_icon_emoji="scrapekot_emoji",
        slack_username="scrapekot_username",
        message="test_message",
        title="test_title",
        color="green",
    )
    fixtures = [Fixture("", notify_data)]
    for fixture in fixtures:
        api._post_slack(fixture.notify_data)


def test_SlackClient__get_message():
    @dataclass
    class Fixture:
        desc: str
        input: AggregatedData
        expected: str

    aggregated_data = AggregatedData(
        work_counts_remain=-1,
        work_counts=-1,
        monthly_work_counts=-1,
        work_hours_remain=-1,
        work_hours=-1,
        monthly_work_hours=-1,
        saving_time=1.25,
        work_hours_remain_by_day=-1,
        start_time="09:00",
        teiji_time="18:00",
    )
    expected = "\n".join([":shigyou:\t09:00", ":teiji:\t18:00", ":bank:\t1時間25分"])
    fixtures = [Fixture("", aggregated_data, expected)]
    for fixture in fixtures:
        actual = api._get_message(fixture.input)
        assert actual == fixture.expected, fixture.desc


def test_SlackClient__get_title():
    dt_now = datetime(2022, 3, 17, 0, 7, 37, 819883)
    expected = "2022/3/17"
    assert api._get_title(dt_now) == expected


def test_SlackClient__get_color():
    @dataclass
    class Fixture:
        desc: str
        input: float
        expected: str

    fixtures = [
        Fixture("saving_timeが1時間以上", 1.0, Color.GREEN.value),
        Fixture("saving_timeが0分以上1時間未満", 0.0, Color.YELLOW.value),
        Fixture("saving_timeがマイナス", -0.1, Color.RED.value),
    ]
    for fixture in fixtures:
        actual = api._get_color(fixture.input)
        assert actual == fixture.expected, fixture.desc


def test_SlackClient__slack_url():
    @dataclass
    class Fixture:
        desc: str
        notify_data: NotifyData
        expected: str

    notify_data = NotifyData(
        slack_webhook_url="scrapekot_url",
        slack_channel="scrapekot_channel",
        slack_icon_emoji="scrapekot_emoji",
        slack_username="scrapekot_username",
        message="test_message",
        title="test_title",
        color="green",
    )
    fixtures = [Fixture("", notify_data, "scrapekot_url")]
    for fixture in fixtures:
        assert api._slack_url(fixture.notify_data) == fixture.expected, fixture.desc


def test_SlackClient__slack_data():
    @dataclass
    class Fixture:
        desc: str
        notify_data: NotifyData
        expected: dict[str, Any]

    notify_data = NotifyData(
        slack_webhook_url="scrapekot_url",
        slack_channel="scrapekot_channel",
        slack_icon_emoji="scrapekot_emoji",
        slack_username="scrapekot_username",
        message="test_message",
        title="test_title",
        color="green",
    )
    expected = {
        "username": "scrapekot_username",
        "icon_emoji": "scrapekot_emoji",
        "channel": "scrapekot_channel",
        "attachments": [
            {
                "pretext": "test_title",
                "color": "green",
                "text": "test_message",
            }
        ],
    }
    fixtures = [Fixture("", notify_data, expected)]
    for fixture in fixtures:
        assert api._slack_data(fixture.notify_data) == fixture.expected, fixture.desc


def test_Console_display(mocker):
    def mock_func_logger_info(message):
        assert message == expected

    aggregated_data = AggregatedData(
        work_counts_remain=8.0,
        work_counts=12.0,
        monthly_work_counts=20.0,
        work_hours_remain=56.0,
        work_hours=104.0,
        monthly_work_hours=160.0,
        saving_time=8.0,
        work_hours_remain_by_day=7.0,
        start_time="09:00",
        teiji_time="18:00",
    )
    dt_today = datetime(2022, 3, 17)
    expected = """
    残り8.0営業日: (12.0/20.0 日)

    あと56時間00分必要: (104時間00分/160時間)

    貯金: 8時間00分

    貯金を元に残り営業日の必要勤務時間数を算出すると: 7時間00分

    {today:%Y-%m-%d}の出勤・定時
        出勤: 09:00
        定時: 18:00
""".format(
        today=dt_today
    )
    mocker.patch("kot.common.logger.logger.info", side_effect=mock_func_logger_info)
    Console.display(aggregated_data, dt_today)


def test_format_hours():
    @dataclass
    class Fixture:
        desc: str
        hours: float
        expected: str

    hours = [
        -1.05,
        1.5,
        1.50,
        0,
    ]
    expected = ["-1時間05分", "1時間50分", "1時間50分", "0時間00分"]
    fixtures = [Fixture("", h, e) for h, e in zip(hours, expected)]
    for fixture in fixtures:
        assert format_hours(fixture.hours) == fixture.expected, fixture.desc
