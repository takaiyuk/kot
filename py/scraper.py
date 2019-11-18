# Import
from collections import Counter
from bs4 import BeautifulSoup

from .const import WORK_HOUR
from .crawler import Crawler


class Scraper:
    def __init__(self):
        self.soup = None
        self.holiday_count = 0  # TODO: 当月利用した有給日数を取得

    def _clean_text(self, x):
        x = x.replace("\n", "")
        x = x.strip()
        return x

    def _hour_to_minute(self, hours):
        return round(hours // 1.0 * 60 + hours % 1.0 * 100)

    def _minute_to_hour(self, minutes):
        return minutes // 60 + round(minutes % 60 / 100, 2)

    def _str_to_int(self, string):
        return int(float(string))

    def calc_monthly_work_hour(self, monthly_work_count):
        return WORK_HOUR * monthly_work_count

    def calc_count_remain(self, monthly_work_count, work_count):
        return monthly_work_count - work_count

    def calc_hour_remain(self, total_hours, finished_hours):
        total_minutes = self._hour_to_minute(total_hours)
        finished_minites = self._hour_to_minute(finished_hours)
        remain_minutes = total_minutes - finished_minites
        remain_hour = self._minute_to_hour(remain_minutes)
        return remain_hour

    def calc_hour_remain_by_day(self, remain_hours, remain_count):
        remain_minutes = self._hour_to_minute(remain_hours)
        remain_minutes_by_day = remain_minutes / remain_count
        remain_hours_by_day = self._minute_to_hour(remain_minutes_by_day)
        return remain_hours_by_day

    def calc_saving_time(self, work_hour, work_count):
        return work_hour - WORK_HOUR * work_count

    def get_monthly_work_count(self):
        work_day_types = []
        for i in range(31):
            try:
                work_day_type = self._clean_text(
                    self.soup.find_all("td", class_="work_day_type")[i].p.string
                )
                work_day_types.append(work_day_type)
            except IndexError:
                break
        c = Counter(work_day_types)
        monthly_work_count = self._str_to_int(c["平日"])
        return monthly_work_count

    def get_work_count(self):
        work_count = self.soup.find("div", class_="work_count").string
        work_count = self._str_to_int(work_count)
        work_count += self.holiday_count
        return work_count

    def get_work_hour(self):
        work_hour = self._clean_text(self.soup.find("td", class_="custom2").string)
        work_hour = float(work_hour)
        yukyu_hour = WORK_HOUR * self.holiday_count
        work_hour += yukyu_hour
        return work_hour

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

        # 今月の必要勤務日を取得
        monthly_work_count = self.get_monthly_work_count()

        # 今月の必要勤務時間を計算
        monthly_work_hours = self.calc_monthly_work_hour(monthly_work_count)

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
        saveing_time = self.calc_saving_time(work_hours, work_count)

        # 当日の出勤打刻時間
        start_time, teiji_time = self.get_today_work_start()

        return {
            "work_count_remain": work_count_remain,
            "work_count": work_count,
            "monthly_work_count": monthly_work_count,
            "work_hour_remain": work_hours_remain,
            "work_hour": work_hours,
            "monthly_work_hour": monthly_work_hours,
            "saveing_time": saveing_time,
            "work_hour_remain_by_day": work_hours_remain_by_day,
            "start_time": start_time,
            "teiji_time": teiji_time,
        }

    def run(self, html=None):
        values = self.raw_data(html=html)

        message1, message2, message3, message4, message5, message6 = [
            x.format(**values)
            for x in (
                "REMAIN-DAYS={work_count_remain}days(done={work_count}/{monthly_work_count})",
                "REMAIN-HOURS={work_hours_remain:.2f}h(done={work_hours}/{monthly_work_hours})",
                ":bank:--{saveing_time:.2f}h",
                "REMAIN-HOURS-BY-DAY={work_hours_remain_by_day:.2f}h",
                ":shigyou:--{start_time}",
                ":teiji:--{teiji_time}",
            )
        ]

        for message in [message1, message2, message3, message4, message5, message6]:
            print(message)

        return [message5, message6, message3]
