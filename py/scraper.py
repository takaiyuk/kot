# Import
from bs4 import BeautifulSoup
from typing import Any, Tuple

WORK_HOUR = 8


class Parser:
    def __init__(self, html: str) -> None:
        if html is not None:
            self.soup = BeautifulSoup(html, "html.parser")
        self.holiday_count = 0.0
        self.monthly_work_hours = 0.0
        self.your_work_hours = 0.0
        self.your_work_count = 0.0
        self.start_time = None
        self.teiji_time = None

    def _str_to_int(self, string: str) -> int:
        """
        文字列(string)を離散値(int)に変更する
        """
        return int(float(string))

    def _clean_text(self, x: str) -> str:
        x = x.replace("\n", "")
        x = x.replace(" ", "")
        x = x.strip()
        return x

    def get_holiday_count(self) -> None:
        """
        有給や半休等の日数を数え上げる
        """
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
        # 年末年始休暇は勤務日種別が法定休日なのでカウントしない
        # self.holiday_count += float(self._clean_text(holiday_counts[5].text))
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
        """
        当月の必要総労働時間（営業日 * 8時間）を取得する
        """
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
        """
        ユーザーの打刻が発生した（即ち有給や半休等を除いた）労働日数を数え上げる
        """
        your_work_count = self.soup.find("div", class_="work_count").string
        your_work_count = float(your_work_count)
        your_work_count += self.holiday_count
        return your_work_count

    def get_your_work_hour(self) -> float:
        """
        ユーザーの前日までの総労働時間（「フレ労働時間」）を取得する
        """
        your_work_hour = self._clean_text(self.soup.find("td", class_="custom3").string)
        try:
            return float(your_work_hour)
        except ValueError:
            # 月初は前日までの勤務時間を取得できないので ValueError になる
            return 0.0

    def get_today_kintai(self) -> Tuple[Any, Any]:
        """
        ユーザーの当日の出勤打刻時間の取得と、8時間勤務した場合の退勤時間の計算を行う
        """
        start_time_string, teiji_time_string = None, None
        try:
            st_string_dirty = self.soup.find_all(
                "td", class_="start_end_timerecord specific-uncomplete"
            )[-2].text
            # 上記の出力例: '\n\n\nIC\n\n09:02\n\n'
            start_time_string = (
                st_string_dirty.split(":")[0][-2:]
                + ":"
                + st_string_dirty.split(":")[1][:2]
            )
            hhmm = start_time_string.split(":")
            teiji_time_string = ":".join(
                [str(self._str_to_int(hhmm[0]) + (WORK_HOUR + 1)), hhmm[1]]
            )
        except Exception:
            start_time_string, teiji_time_string = None, None
            print("打刻しましたか？退勤後なら問題ないですが")
        finally:
            return start_time_string, teiji_time_string

    def parse(self) -> None:
        # 有給等の取得日数を取得
        self.get_holiday_count()

        # 今月の必要勤務時間を取得
        self.monthly_work_hours = self.get_monthly_work_hour()

        # 前日までの勤務時間を取得
        self.your_work_hours = self.get_your_work_hour()

        # 前日までの勤務日数を取得
        self.your_work_count = self.get_your_work_count()

        # 当日の出勤打刻時間
        self.start_time, self.teiji_time = self.get_today_kintai()


class Aggregator:
    def __init__(self) -> None:
        self.monthly_work_count = 0.0
        self.your_work_hours_remain = 0.0
        self.your_work_count_remain = 0.0
        self.your_work_hours_remain_by_day = 0.0
        self.saving_time = 0.0

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
        """
        is_minus = False
        if minutes < 0:
            is_minus = True
            minutes *= -1
        hm = minutes // 60 + round(minutes % 60 / 100, 2)
        if is_minus:
            hm *= -1
        return round(hm, 2)

    def _diff_hours(self, h1: float, h2: float) -> float:
        """
        (ex.)
        Parameters
        ----------
        h1: 18.45(=18h45m)
        h2: 16.0(=16h00m)

        Returns
        -------
        h1 - h2: 2.45(=2h45m)
        """
        m1 = self._hour_to_minute(h1)
        m2 = self._hour_to_minute(h2)
        m_diff = m1 - m2
        h_diff = self._minute_to_hour(m_diff)
        return round(h_diff, 2)

    def calc_monthly_work_count(self, monthly_work_hour: float) -> float:
        """
        当月の営業日数を必要総労働時間から割り出す
        """
        monthly_work_count = monthly_work_hour / WORK_HOUR
        return round(monthly_work_count, 2)

    def calc_count_remain(self, monthly_work_count: float, work_count: float) -> float:
        """
        当月の残り営業日数
        """
        return round(monthly_work_count - work_count, 2)

    def calc_hour_remain(self, total_hours: float, finished_hours: float) -> float:
        """
        当月の残り必要勤務時間
        """
        remain_hour = self._diff_hours(total_hours, finished_hours)
        return remain_hour

    def calc_hour_remain_by_day(
        self, remain_hours: float, remain_count: float
    ) -> float:
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

    def aggregate(self, parser: Parser) -> None:
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
    def __init__(self, html) -> None:
        self.parser = Parser(html)
        self.aggregator = Aggregator()

    def _change_notation(self, str_time: Any) -> str:
        """
        2.31 -> 2時間31分
        2.5 -> 2時間50分
        2.50 -> 2時間50分
        """
        str_time = str(str_time)
        hh = str_time.split(".")[0]
        mm = str_time.split(".")[1]
        # 2.5 -> 2時間5分となってしまうのを回避する(本来は 2.5 = 2.50 -> 2時間50分なので)
        if len(mm) == 1:
            mm += "0"
        return f"{hh}時間{mm}分"

    def raw_data(self) -> Tuple[dict, float]:
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
                self.aggregator.your_work_hours_remain_by_day
            ),
            "start_time": self.parser.start_time,
            "teiji_time": self.parser.teiji_time,
        }

        return (results, self.aggregator.saving_time)

    def scrape(self) -> Tuple[list, float]:
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

        notify_messages = [message5, message6, message3]

        return notify_messages, saving_time
