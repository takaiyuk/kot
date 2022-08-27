from dataclasses import dataclass

from kot.scrapekot.scrape import ScrapedData

WORK_HOUR = 8


@dataclass
class AggregatedData:
    work_counts_remain: float
    work_counts: float
    monthly_work_counts: float
    work_hours_remain: float
    work_hours: float
    monthly_work_hours: float
    saving_time: float
    work_hours_remain_by_day: float
    start_time: str
    teiji_time: str


class Aggregator:
    def aggregate(self, scraped_data: ScrapedData) -> AggregatedData:
        # 今月の必要勤務日を計算
        monthly_work_counts = self.calc_monthly_work_counts(scraped_data.monthly_work_hours)

        # 残り日数を計算
        work_hours_remain = self.calc_work_hours_remain(
            scraped_data.monthly_work_hours, scraped_data.work_hours
        )

        # 残り必要時間を計算
        work_counts_remain = self.calc_work_counts_remain(monthly_work_counts, scraped_data.work_counts)

        # 1日あたりの必要時間を計算
        work_hours_remain_by_day = self.calc_work_hours_remain_by_day(work_hours_remain, work_counts_remain)

        # 貯金時間を計算
        saving_time = self.calc_saving_time(scraped_data.work_hours, scraped_data.work_counts)

        aggregated_data = AggregatedData(
            work_counts_remain=work_counts_remain,
            work_counts=scraped_data.work_counts,
            monthly_work_counts=monthly_work_counts,
            work_hours_remain=work_hours_remain,
            work_hours=scraped_data.work_hours,
            monthly_work_hours=scraped_data.monthly_work_hours,
            saving_time=saving_time,
            work_hours_remain_by_day=work_hours_remain_by_day,
            start_time=scraped_data.start_time,
            teiji_time=scraped_data.teiji_time,
        )
        return aggregated_data

    def calc_monthly_work_counts(self, monthly_work_hour: float) -> float:
        """
        当月の営業日数を必要総労働時間から割り出す
        """
        monthly_work_count = monthly_work_hour / WORK_HOUR
        return round(monthly_work_count, 2)

    def calc_work_hours_remain(self, total_hours: float, finished_hours: float) -> float:
        """
        当月の残り必要勤務時間
        """
        remain_hour = self._diff_hours(total_hours, finished_hours)
        return remain_hour

    def calc_work_counts_remain(self, monthly_work_count: float, work_count: float) -> float:
        """
        当月の残り営業日数
        """
        return round(monthly_work_count - work_count, 2)

    def calc_work_hours_remain_by_day(self, remain_hours: float, remain_count: float) -> float:
        """
        当月の1日あたりの残り必要勤務時間
        """
        remain_minutes = self._hour_to_minute(remain_hours)
        try:
            remain_minutes_by_day = remain_minutes / remain_count
            remain_hours_by_day = self._minute_to_hour(remain_minutes_by_day)
        except ZeroDivisionError:
            # 労働基準時間が設定されてないと当月の残り営業日数（remain_count）が0になる
            remain_hours_by_day = 0.0
        return remain_hours_by_day

    def calc_saving_time(self, work_hour: float, work_count: float) -> float:
        saving_time = self._diff_hours(work_hour, WORK_HOUR * work_count)
        return saving_time

    def _hour_to_minute(self, hours: float) -> float:
        """
        (ex.)
        1.24(=1h24m) -> 84
        -1.24(=1h24m) -> -84
        """
        is_minus = False
        if hours < 0:
            is_minus = True
            hours *= -1
        minutes = round(hours // 1.0 * 60 + hours % 1.0 * 100)
        if is_minus:
            minutes *= -1
        return round(minutes, 2)

    def _minute_to_hour(self, minutes: float) -> float:
        """
        (ex.)
        84 -> 1.24(=1h24m)
        -84 -> -1.24(=-1h24m)
        479.875 -> 7.59875(=7h59.875m) -> 7.60 -> 8h00m
        """
        is_minus = False
        if minutes < 0:
            is_minus = True
            minutes *= -1
        hm = minutes // 60 + round(minutes % 60 / 100, 2)
        if is_minus:
            hm *= -1
        hm = round(hm, 2)
        if round(hm % 1, 2) == 0.6:
            return float(round(hm))
        else:
            return hm

    def _diff_hours(self, h1: float, h2: float) -> float:
        """
        (ex.)
        Parameters
        ----------
        h1: 18.0(=18h00m)
        h2: 16.45(=16h45m)

        Returns
        -------
        h1 - h2: 1.15(=1h15m)
        """
        m1 = self._hour_to_minute(h1)
        m2 = self._hour_to_minute(h2)
        m_diff = m1 - m2
        h_diff = self._minute_to_hour(m_diff)
        return round(h_diff, 2)
