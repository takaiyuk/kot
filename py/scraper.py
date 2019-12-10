# Import
from bs4 import BeautifulSoup
from collections import Counter

from .const import WORK_HOUR
from .crawler import Crawler


class Scraper:
    def __init__(self):
        self.soup = None
        self.holiday_count = 0  # TODO: 当月利用した有給日数を取得

    def _clean_text(self, x):
        x = x.replace("\n", "")
        x = x.replace(" ", "")
        x = x.strip()
        return x

    def _hour_to_minute(self, hours):
        return round(hours // 1.0 * 60 + hours % 1.0 * 100)

    def _minute_to_hour(self, minutes):
        return minutes // 60 + round(minutes % 60 / 100, 2)

    def _str_to_int(self, string):
        return int(float(string))

    def _change_notation(self, str_time):
        """
        2.31 -> 2時間31分
        """
        str_time = str(str_time)
        return f'{str_time.split(".")[0]}時間{str_time.split(".")[1]}分'

    def calc_monthly_work_count(self, monthly_work_hour):
        monthly_work_count = monthly_work_hour / WORK_HOUR
        return round(monthly_work_count, 2)

    def calc_count_remain(self, monthly_work_count, work_count):
        return round(monthly_work_count - work_count, 2)

    def calc_hour_remain(self, total_hours, finished_hours):
        total_minutes = self._hour_to_minute(total_hours)
        finished_minites = self._hour_to_minute(finished_hours)
        remain_minutes = total_minutes - finished_minites
        remain_hour = self._minute_to_hour(remain_minutes)
        return round(remain_hour, 2)

    def calc_hour_remain_by_day(self, remain_hours, remain_count):
        remain_minutes = self._hour_to_minute(remain_hours)
        remain_minutes_by_day = remain_minutes / remain_count
        remain_hours_by_day = self._minute_to_hour(remain_minutes_by_day)
        return round(remain_hours_by_day, 2)

    def calc_saving_time(self, work_hour, work_count):
        saving_time = work_hour - WORK_HOUR * work_count
        return round(saving_time, 2)

    def get_holiday_count(self):
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

    def get_monthly_work_hour(self):
        monthly_work_hour = (
            self.soup.find("table", class_="specific-table_800")
            .find("tbody")
            .find("tr")
            .find("td")
            .text
        )
        monthly_work_hour = self._clean_text(monthly_work_hour)
        return float(monthly_work_hour)

    def get_work_count(self):
        work_count = self.soup.find("div", class_="work_count").string
        work_count = float(work_count)
        work_count += self.holiday_count
        return work_count

    def get_work_hour(self):
        work_hour = self._clean_text(self.soup.find("td", class_="custom3").string)
        try:
            return float(work_hour)
        except ValueError:
            # 月初は前日までの勤務時間を取得できないので ValueError になる
            return 0

    def get_today_work_start(self):
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

    def raw_data(self, html=None):
        if html is None:
            html = Crawler().get_source()
        self.soup = BeautifulSoup(html, "html.parser")

        # 有給等の取得日数を取得
        self.get_holiday_count()

        # 今月の必要勤務時間を取得
        monthly_work_hours = self.get_monthly_work_hour()

        # 今月の必要勤務日を計算
        monthly_work_count = self.calc_monthly_work_count(monthly_work_hours)

        # 前日までの勤務日数を取得
        work_count = self.get_work_count()

        # 前日までの勤務時間を取得
        work_hours = self.get_work_hour()

        # 残り日数と残り必要時間、1日あたりの必要時間を計算
        work_count_remain = self.calc_count_remain(monthly_work_count, work_count)
        work_hours_remain = self.calc_hour_remain(monthly_work_hours, work_hours)
        work_hours_remain_by_day = self.calc_hour_remain_by_day(
            work_hours_remain, work_count_remain
        )

        # 暫定残業時間を計算
        saving_time = self.calc_saving_time(work_hours, work_count)

        # 当日の出勤打刻時間
        try:
            start_time, teiji_time = self.get_today_work_start()
        except Exception:
            print("打刻しましたか？退勤後なら問題ないですが")
            start_time, teiji_time = None, None

        results = {
            "work_count_remain": work_count_remain,
            "work_count": work_count,
            "monthly_work_count": monthly_work_count,
            "work_hours_remain": self._change_notation(work_hours_remain),
            "work_hours": self._change_notation(work_hours),
            "monthly_work_hours": self._change_notation(monthly_work_hours),
            "saving_time": self._change_notation(saving_time),
            "work_hours_remain_by_day": self._change_notation(work_hours_remain_by_day),
            "start_time": start_time,
            "teiji_time": teiji_time,
        }

        return (results, saving_time)

    def run(self, html=None):
        values, saving_time = self.raw_data(html=html)

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
