import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from scraper import Aggregator, Scraper


def test_aggregator_hour_to_minute():
    hours = 1.35
    minutes = Aggregator()._hour_to_minute(hours)
    assert minutes == 95

    hours = 0.0
    minutes = Aggregator()._hour_to_minute(hours)
    assert minutes == 0.0

    hours = -1.35
    minutes = Aggregator()._hour_to_minute(hours)
    assert minutes == -95


def test_aggregator_minute_to_hour():
    minutes = 95
    hours = Aggregator()._minute_to_hour(minutes)
    assert hours == 1.35

    minutes = 0
    hours = Aggregator()._minute_to_hour(minutes)
    assert hours == 0.0

    minutes = -95
    hours = Aggregator()._minute_to_hour(minutes)
    assert hours == -1.35


def test_aggregator_diff_hours():
    h1 = 18.45
    h2 = 16.0
    diff = Aggregator()._diff_hours(h1, h2)
    assert diff == 2.45

    h1 = 16.0
    h2 = 16.0
    diff = Aggregator()._diff_hours(h1, h2)
    assert diff == 0

    h1 = 14.45
    h2 = 16.0
    diff = Aggregator()._diff_hours(h1, h2)
    assert diff == -1.15


def test_aggregator_calc_monthly_work_count():
    monthly_work_count = Aggregator().calc_monthly_work_count(160)
    assert monthly_work_count == 20


def test_aggregator_calc_count_remain():
    count_remain = Aggregator().calc_count_remain(20, 12)
    assert count_remain == 8


def test_aggregator_calc_hour_remain():
    calc_hour_remain = Aggregator().calc_hour_remain(160, 105.50)
    assert calc_hour_remain == 54.10


def test_aggregator_calc_hour_remain_by_day():
    calc_hour_remain_by_day = Aggregator().calc_hour_remain_by_day(54.10, 8)
    assert calc_hour_remain_by_day == 6.46

    calc_hour_remain_by_day = Aggregator().calc_hour_remain_by_day(0, 0)
    assert calc_hour_remain_by_day == 0.0


def test_aggregator_calc_saving_time():
    calc_saving_time = Aggregator().calc_saving_time(89.50, 10)
    assert calc_saving_time == 9.50

    calc_saving_time = Aggregator().calc_saving_time(77.50, 10)
    assert calc_saving_time == -2.10


def test_scraper_change_notation():
    change_notation = Scraper(None)._change_notation("2.31")
    assert change_notation == "2時間31分"

    change_notation = Scraper(None)._change_notation("2.5")
    assert change_notation == "2時間50分"

    change_notation = Scraper(None)._change_notation("2.50")
    assert change_notation == "2時間50分"

    change_notation = Scraper(None)._change_notation("2.05")
    assert change_notation == "2時間05分"

    change_notation = Scraper(None)._change_notation("-2.31")
    assert change_notation == "-2時間31分"

    change_notation = Scraper(None)._change_notation("-2.5")
    assert change_notation == "-2時間50分"

    change_notation = Scraper(None)._change_notation("-2.50")
    assert change_notation == "-2時間50分"

    change_notation = Scraper(None)._change_notation("-2.05")
    assert change_notation == "-2時間05分"
