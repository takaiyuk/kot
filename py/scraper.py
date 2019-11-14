# Import
from collections import Counter
from bs4 import BeautifulSoup

from .const import WORK_HOUR
from .crawler import Crawler


class Scraper:
    def __init__(self):
        self.soup = None

    def clean_text(self, x):
        x = x.replace("\n", "")
        x = x.strip()
        return x

    def str_to_int(self, string):
        return int(float(string))

    def calc_monthly_work_hour(self, monthly_work_count):
        return WORK_HOUR * monthly_work_count

    def calc_count_remain(self, monthly_work_count, work_count):
        return monthly_work_count - work_count

    def calc_hour_remain(self, total_hour, finished_hour):
        total_minutes = total_hour * 60
        finished_minites = round(finished_hour // 1.0 * 60 + finished_hour % 1.0 * 100)
        remain_minutes = total_minutes - finished_minites
        remain_hour = remain_minutes // 60 + round(remain_minutes % 60 / 100, 2)
        return remain_hour

    def calc_hour_remain_by_day(self, remain_hour, remain_count):
        remain_min = remain_hour * 60
        remain_min_by_day = remain_min / remain_count
        remain_hour_by_day = remain_min_by_day // 60 + round(
            remain_min_by_day % 60 / 100, 2
        )
        return remain_hour_by_day

    def calc_saving_time(self, work_hour, work_count):
        return work_hour - WORK_HOUR * work_count

    def get_monthly_work_count(self):
        work_day_types = []
        for i in range(31):
            try:
                work_day_type = self.clean_text(
                    self.soup.find_all("td", class_="work_day_type")[i].p.string
                )
                work_day_types.append(work_day_type)
            except IndexError:
                break
        c = Counter(work_day_types)
        monthly_work_count = self.str_to_int(c["平日"])
        return monthly_work_count

    def get_work_count(self, yukyu_count):
        work_count = self.soup.find("div", class_="work_count").string
        work_count = self.str_to_int(work_count)
        work_count += yukyu_count
        return work_count

    def get_work_hour(self, yukyu_count):
        work_hour = self.clean_text(self.soup.find("td", class_="custom2").string)
        work_hour = float(work_hour)
        yukyu_hour = WORK_HOUR * yukyu_count
        work_hour += yukyu_hour
        return work_hour

    def get_today_work_start(self):
        start_time_string = self.clean_text(
            self.soup.find("td", class_="start_end_timerecord specific-uncomplete").text
        ).replace("IC", "")
        hhmm = start_time_string.split(":")
        teiji_time_string = ":".join([str(int(hhmm[0]) + (WORK_HOUR + 1)), hhmm[1]])
        return start_time_string, teiji_time_string

    def raw_data(self, html=None):
        if html is None:
            html = Crawler().get_source()
        self.soup = BeautifulSoup(html, "html.parser")
        yukyu_count = 0  # TODO: 当月利用した有給日数を取得

        # 今月の必要勤務日を取得
        monthly_work_count = self.get_monthly_work_count()

        # 今月の必要勤務時間を計算
        monthly_work_hour = self.calc_monthly_work_hour(monthly_work_count)

        # 前日までの勤務日数を取得
        work_count = self.get_work_count(yukyu_count)

        # 前日までの勤務時間を取得
        work_hour = self.get_work_hour(yukyu_count)

        # 残り日数と残り必要時間、1日あたりの必要時間を計算
        work_count_remain = self.calc_count_remain(monthly_work_count, work_count)
        work_hour_remain = self.calc_hour_remain(monthly_work_hour, work_hour)
        work_hour_remain_by_day = self.calc_hour_remain_by_day(
            work_hour_remain, work_count_remain
        )

        # 暫定残業時間を計算
        saveing_time = self.calc_saving_time(work_hour, work_count)

        # 当日の出勤打刻時間
        start_time, teiji_time = self.get_today_work_start()

        return {
            "work_count_remain": work_count_remain,
            "work_count": work_count,
            "monthly_work_count": monthly_work_count,
            "work_hour_remain": work_hour_remain,
            "work_hour": work_hour,
            "monthly_work_hour": monthly_work_hour,
            "saveing_time": saveing_time,
            "work_hour_remain_by_day": work_hour_remain_by_day,
            "start_time": start_time,
            "teiji_time": teiji_time,
        }

    def run(self, html=None):
        values = self.raw_data(html=html)

        message1, message2, message3, message4, message5, message6 = [
            x.format(**values)
            for x in (
                "REMAIN-DAYS={work_count_remain}days(done={work_count}/{monthly_work_count})",
                "REMAIN-HOURS={work_hour_remain:.2f}h(done={work_hour}/{monthly_work_hour})",
                ":bank:--{saveing_time:.2f}h",
                "REMAIN-HOURS-BY-DAY={work_hour_remain_by_day:.2f}h",
                ":shigyou:--{start_time}",
                ":teiji:--{teiji_time}",
            )
        ]

        for message in [message1, message2, message3, message4, message5, message6]:
            print(message)

        return [message5, message6, message3]
