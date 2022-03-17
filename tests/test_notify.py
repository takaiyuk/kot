import json
from dataclasses import dataclass
from datetime import datetime

from kot.aggregate import AggregatedData
from kot.config import Account, Config, MyRecorder, ScrapeKOT, Slack
from kot.notify import Color, Console, NotifyData, SlackClient

api = SlackClient()


def test_SlackClient_notify():
    pass


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
    expected = "\n".join([":shigyou:\t09:00", ":teiji:\t18:00", ":bank:\t1.25"])
    fixtures = [Fixture("", aggregated_data, expected)]
    for fixture in fixtures:
        actual = api._get_message(fixture.input)
        assert actual == fixture.expected, fixture.desc


def test_SlackClient__post_slack(mocker):
    @dataclass
    class Fixture:
        desc: str
        cfg: Config
        notify_data: NotifyData

    def mock_func_requests_post(url, data):
        assert url == "scrapekot_url"
        assert data == json.dumps(
            {
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
    notify_data = NotifyData(title="test_title", message="test_message", color="green")
    fixtures = [Fixture("", cfg, notify_data)]
    for fixture in fixtures:
        api._post_slack(fixture.cfg, fixture.notify_data)


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

    あと56.0必要: (104.0/160.0)

    貯金: 8.0

    貯金を元に残り営業日の必要勤務時間数を算出すると: 7.0

    {today:%Y-%m-%d}の出勤・定時
        出勤: 09:00
        定時: 18:00
""".format(
        today=dt_today
    )
    mocker.patch("kot.logger.logger.info", side_effect=mock_func_logger_info)
    Console.display(aggregated_data, dt_today)
