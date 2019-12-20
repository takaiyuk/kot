# Import
from bs4 import BeautifulSoup
from typing import Tuple

from .const import WORK_HOUR
from .crawler import Crawler


class Parser:
    def __init__(self, html: str) -> None:
        self.soup = BeautifulSoup(html, "html.parser")
        self.holiday_count = 0.0
        self.monthly_work_hours = 0.0
        self.your_work_hours = 0.0
        self.your_work_count = 0.0
        self.start_time = None
        self.teiji_time = None

    def _str_to_int(self, string) -> int:
        return int(float(string))

    def get_holiday_count(self) -> None:
        holiday_counts = self.soup.find_all("div", class_="holiday_count")
        # 有給
        self.holiday_count += float(
            self._clean_text(holiday_counts[0].text).split("(")[0]
        )
        # 代休
        self.holiday_count += float(
            self._clean_text(holiday_counts[1].text).split("(")[0]
        )
        # 夏季休暇
        self.holiday_count += float(
            self._clean_text(holiday_counts[3].text).split("(")[0]
        )
        # 特別休暇
        self.holiday_count += float(
            self._clean_text(holiday_counts[4].text).split("/")[0]
        )
        # 年末年始休暇
        self.holiday_count += float(self._clean_text(holiday_counts[5].text))
        # 輪番休暇
        self.holiday_count += float(
            self._clean_text(holiday_counts[6].text).split("(")[0]
        )
        # 産休・育休
        self.holiday_count += float(self._clean_text(holiday_counts[7].text))
        # 代休（土曜日・祝日）
        self.holiday_count += float(
            self._clean_text(holiday_counts[8].text).split("(")[0]
        )
        # 代休（日曜日）
        self.holiday_count += float(
            self._clean_text(holiday_counts[9].text).split("(")[0]
        )
        # 特別輪番休暇
        self.holiday_count += float(
            self._clean_text(holiday_counts[10].text).split("(")[0]
        )

    def get_monthly_work_hour(self) -> float:
        monthly_work_hour = (
            self.soup.find("table", class_="specific-table_800")
            .find("tbody")
            .find("tr")
            .find("td")
            .text
        )
        monthly_work_hour = self._clean_text(monthly_work_hour)
        return float(monthly_work_hour)

    def get_your_work_count(self) -> float:
        your_work_count = self.soup.find("div", class_="work_count").string
        your_work_count = float(your_work_count)
        your_work_count += self.holiday_count
        return your_work_count

    def get_your_work_hour(self) -> float:
        your_work_hour = self._clean_text(self.soup.find("td", class_="custom3").string)
        try:
            return float(your_work_hour)
        except ValueError:
            # 月初は前日までの勤務時間を取得できないので ValueError になる
            return 0.0

    def get_today_kintai(self) -> Tuple[str, str]:
        start_time_string = self._clean_text(
            self.soup.find_all("td", class_="start_end_timerecord specific-uncomplete")[
                -2
            ].text
        )
        ic_place = start_time_string.find("IC")
        start_time_string = start_time_string[(ic_place + 2) : (ic_place + 7)]
        hhmm = start_time_string.split(":")
        teiji_time_string = ":".join(
            [str(self._str_to_int(hhmm[0]) + (WORK_HOUR + 1)), hhmm[1]]
        )
        return start_time_string, teiji_time_string

    def parse(self):
        # 有給等の取得日数を取得
        self.get_holiday_count()

        # 今月の必要勤務時間を取得
        self.monthly_work_hours = self.get_monthly_work_hour()

        # 前日までの勤務時間を取得
        self.your_work_hours = self.get_your_work_hour()

        # 前日までの勤務日数を取得
        self.your_work_count = self.get_your_work_count()

        # 当日の出勤打刻時間
        try:
            self.start_time, self.teiji_time = self.get_today_kintai()
        except Exception:
            print("打刻しましたか？退勤後なら問題ないですが")


class Aggregator:
    def __init__(self) -> None:
        self.monthly_work_count = 0.0
        self.your_work_hours_remain = 0.0
        self.your_work_count_remain = 0.0
        self.your_work_hours_remain_by_day = 0.0
        self.saving_time = 0.0

    def _clean_text(self, x: str) -> str:
        x = x.replace("\n", "")
        x = x.replace(" ", "")
        x = x.strip()
        return x

    def _hour_to_minute(self, hours: float) -> float:
        return round(hours // 1.0 * 60 + hours % 1.0 * 100)

    def _minute_to_hour(self, minutes: float) -> float:
        is_minus = False
        if minutes < 0:
            is_minus = True
            minutes *= -1
        hm = minutes // 60 + round(minutes % 60 / 100, 2)
        if is_minus:
            hm *= -1
        return round(hm, 2)

    def _diff_hours(self, h1: float, h2: float) -> float:
        m1 = self._hour_to_minute(h1)
        m2 = self._hour_to_minute(h2)
        m_diff = m1 - m2
        h_diff = self._minute_to_hour(m_diff)
        return round(h_diff, 2)

    def calc_monthly_work_count(self, monthly_work_hour: float) -> float:
        monthly_work_count = monthly_work_hour / WORK_HOUR
        return round(monthly_work_count, 2)

    def calc_count_remain(self, monthly_work_count: float, work_count: float) -> float:
        return round(monthly_work_count - work_count, 2)

    def calc_hour_remain(self, total_hours: float, finished_hours: float) -> float:
        remain_hour = self._diff_hours(total_hours, finished_hours)
        return remain_hour

    def calc_hour_remain_by_day(
        self, remain_hours: float, remain_count: float
    ) -> float:
        remain_minutes = self._hour_to_minute(remain_hours)
        remain_minutes_by_day = remain_minutes / remain_count
        remain_hours_by_day = self._minute_to_hour(remain_minutes_by_day)
        return remain_hours_by_day

    def calc_saving_time(self, work_hour: float, work_count: float) -> float:
        saving_time = self._diff_hours(work_hour, WORK_HOUR * work_count)
        return saving_time

    def aggregate(self, parser: Parser):
        # 今月の必要勤務日を計算
        self.monthly_work_count = self.calc_monthly_work_count(
            parser.monthly_work_hours
        )

        # 残り日数を計算
        self.your_work_hours_remain = self.calc_hour_remain(
            parser.monthly_work_hours, parser.your_work_hours
        )

        # 残り必要時間を計算
        self.your_work_count_remain = self.calc_count_remain(
            self.monthly_work_count, parser.your_work_count
        )

        # 1日あたりの必要時間を計算
        self.your_work_hours_remain_by_day = self.calc_hour_remain_by_day(
            self.your_work_hours_remain, self.your_work_count_remain
        )

        # 貯金時間を計算
        self.saving_time = self.calc_saving_time(
            parser.your_work_hours, parser.your_work_count
        )


class Scraper:
    def __init__(self, html: str = None) -> None:
        if html is None:
            html = Crawler().get_source()
        self.parser = Parser(html)
        self.aggregator = Aggregator()

    def _change_notation(self, str_time: str) -> str:
        """
        2.31 -> 2時間31分
        """
        str_time = str(str_time)
        return f'{str_time.split(".")[0]}時間{str_time.split(".")[1]}分'

    def raw_data(self):
        self.parser.parse()
        self.aggregator.aggregate(self.parser)

        results = {
            "work_count_remain": self.aggregator.your_work_count_remain,
            "work_count": self.parser.your_work_count,
            "monthly_work_count": self.aggregator.monthly_work_count,
            "work_hours_remain": self._change_notation(
                self.aggregator.your_work_hours_remain
            ),
            "work_hours": self._change_notation(self.parser.your_work_hours),
            "monthly_work_hours": self._change_notation(self.parser.monthly_work_hours),
            "saving_time": self._change_notation(self.aggregator.saving_time),
            "work_hours_remain_by_day": self._change_notation(
                self.aggregator.work_hours_remain_by_day
            ),
            "start_time": self.parser.start_time,
            "teiji_time": self.parser.teiji_time,
        }

        return (results, self.aggregator.saving_time)

    def run(self):
        values, saving_time = self.raw_data()

        message1, message2, message3, message4, message5, message6 = [
            x.format(**values)
            for x in (
                "残り営業日\t{work_count_remain}days(done={work_count}/{monthly_work_count})",
                "残り必要時間\t{work_hours_remain}(done={work_hours}/{monthly_work_hours})",
                ":bank:\t{saving_time}",
                "1日あたりの残り必要時間\t{work_hours_remain_by_day}",
                ":shigyou:\t{start_time}",
                ":teiji:\t{teiji_time}",
            )
        ]

        for message in [message1, message2, message3, message4, message5, message6]:
            print(message)

        return [message5, message6, message3], saving_time
