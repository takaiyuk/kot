from dataclasses import dataclass

from kot.scrapekot.aggregate import AggregatedData, Aggregator
from kot.scrapekot.scrape import ScrapedData

a = Aggregator()


def test_Aggregator_aggregate():
    @dataclass
    class Fixture:
        desc: str
        input: ScrapedData
        expected: AggregatedData

    input = ScrapedData(
        holiday_counts=0.0,
        monthly_work_hours=160.0,
        work_hours=104.0,
        work_counts=12.0,
        start_time="09:00",
        teiji_time="18:00",
    )
    expected = AggregatedData(
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
    fixtures = [Fixture("", input, expected)]
    for fixture in fixtures:
        assert a.aggregate(fixture.input) == fixture.expected, fixture.desc


def test_Aggregator_calc_monthly_work_counts():
    @dataclass
    class Fixture:
        desc: str
        input: float
        expected: float

    fixtures = [Fixture("160h -> 20d", 160.0, 20.0)]
    for fixture in fixtures:
        assert (
            a.calc_monthly_work_counts(fixture.input) == fixture.expected
        ), fixture.desc


def test_Aggregator_calc_work_hours_remain():
    @dataclass
    class Fixture:
        desc: str
        total_hours: float
        finished_hours: float
        expected: float

    fixtures = [Fixture("160h - 105h50m = 54h10m", 160.0, 105.50, 54.10)]
    for fixture in fixtures:
        assert (
            a.calc_work_hours_remain(fixture.total_hours, fixture.finished_hours)
            == fixture.expected
        ), fixture.desc


def test_Aggregator_calc_work_counts_remain():
    @dataclass
    class Fixture:
        desc: str
        monthly_work_count: float
        work_count: float
        expected: float

    fixtures = [Fixture("20d - 8d = 12d", 20, 8, 12)]
    for fixture in fixtures:
        assert (
            a.calc_work_counts_remain(fixture.monthly_work_count, fixture.work_count)
            == fixture.expected
        ), fixture.desc


def test_Aggregator_calc_work_hours_remain_by_day():
    @dataclass
    class Fixture:
        desc: str
        remain_hours: float
        remain_count: float
        expected: float

    fixtures = [Fixture("54.10h / 8d = 6.46h/d", 54.10, 8, 6.46)]
    for fixture in fixtures:
        assert (
            a.calc_work_hours_remain_by_day(fixture.remain_hours, fixture.remain_count)
            == fixture.expected
        ), fixture.desc


def test_Aggregator_calc_saving_time():
    @dataclass
    class Fixture:
        desc: str
        work_hour: float
        work_count: float
        expected: float

    fixtures = [
        Fixture("89.50 - 10 * 8 = 9.50", 89.50, 10, 9.50),
        Fixture("77.50 - 10 * 8 = -2.10", 77.50, 10, -2.10),
    ]
    for fixture in fixtures:
        assert (
            a.calc_saving_time(fixture.work_hour, fixture.work_count)
            == fixture.expected
        ), fixture.desc


def test_Aggregator__hour_to_minute():
    @dataclass
    class Fixture:
        desc: str
        input: float
        expected: float

    fixtures = [
        Fixture("1h24m -> 84m", 1.24, 84.0),
        Fixture("-1h24m -> -84m", -1.24, -84.0),
    ]
    for fixture in fixtures:
        assert a._hour_to_minute(fixture.input) == fixture.expected, fixture.desc


def test_Aggregator__minute_to_hour():
    @dataclass
    class Fixture:
        desc: str
        input: float
        expected: float

    fixtures = [
        Fixture("84m -> 1h24m", 84.0, 1.24),
        Fixture("-84m -> -1h24m", -84.0, -1.24),
    ]
    for fixture in fixtures:
        assert a._minute_to_hour(fixture.input) == fixture.expected, fixture.desc


def test_Aggregator__diff_hours():
    @dataclass
    class Fixture:
        desc: str
        h1: float
        h2: float
        expected: float

    fixtures = [
        Fixture("18h00m - 16h45m = 1h15m", 18.0, 16.45, 1.15),
    ]
    for fixture in fixtures:
        assert a._diff_hours(fixture.h1, fixture.h2) == fixture.expected, fixture.desc
