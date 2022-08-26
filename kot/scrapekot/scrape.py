from dataclasses import dataclass
from typing import Tuple

from bs4 import BeautifulSoup

from kot.common.logger import logger
from kot.scrapekot.crawl import CrawledData

WORK_HOUR = 8


@dataclass
class ScrapedData:
    holiday_counts: float
    monthly_work_hours: float
    work_hours: float
    work_counts: float
    start_time: str
    teiji_time: str


class Scraper:
    def __init__(self, crawled_data: CrawledData) -> None:
        self.soup = BeautifulSoup(crawled_data.page_source, "html.parser")

    def extract(self) -> ScrapedData:
        # 今月の必要勤務時間を取得
        monthly_work_hours = self.get_monthly_work_hours()

        # 有給等の取得日数を取得
        holiday_counts = self.get_holiday_counts()

        # 前日までの勤務日数を取得
        work_counts = self.get_work_counts(holiday_counts)

        # 前日までの勤務時間を取得
        work_hours = self.get_work_hours()

        # 当日の出勤打刻時間
        start_time, teiji_time = self.get_today_kintai()

        scraped_data = ScrapedData(
            holiday_counts=holiday_counts,
            monthly_work_hours=monthly_work_hours,
            work_hours=work_hours,
            work_counts=work_counts,
            start_time=start_time,
            teiji_time=teiji_time,
        )
        return scraped_data

    def get_holiday_counts(self) -> float:
        """
        有給や半休等の日数を数え上げる
        """
        holiday_counts = 0.0
        results = self.soup.find("ul", class_="specific-daysCount_1").find_all("li")
        for result in results:
            label = result.find("label", class_="holiday_count")
            value = result.find("div", class_="holiday_count")
            if label is None or value is None:
                continue
            label = self._clean_text(label.text)
            value = self._clean_text(value.text)
            match label:
                case "有休":
                    holiday_counts += float(value.split("(")[0])
                case "代休":
                    holiday_counts += float(value.split("(")[0])
                # 欠勤はカウントしない
                case "夏季休暇":
                    holiday_counts += float(value.split("(")[0])
                # 年末年始休暇は勤務日種別が法定休日なのでカウントしない
                # 特別休暇（減算）はカウントしない
                case "輪番休暇":
                    holiday_counts += float(value.split("(")[0])
                case "特別輪番休暇":
                    holiday_counts += float(value.split("(")[0])
                case "【メンテ用】特別輪番休暇":
                    holiday_counts += float(value.split("(")[0])
                case "産休・育休":
                    holiday_counts += float(value)
                case "振替休日":
                    holiday_counts += float(value.split("(")[0])
                case "コロナ全日休業":
                    holiday_counts += float(value.split("/")[0])
                case "全日休業":
                    holiday_counts += float(value.split("(")[0])
                case "特別休暇":
                    holiday_counts += float(value.split("/")[0])
        return holiday_counts

    def get_monthly_work_hours(self) -> float:
        """
        当月の必要総労働時間（営業日 * 8時間）を取得する
        """
        monthly_work_hours = (
            self.soup.find("table", class_="specific-table_800").find("tbody").find("tr").find("td").text
        )
        return float(self._clean_text(monthly_work_hours))

    def get_work_counts(self, holiday_counts: float) -> float:
        """
        ユーザーの打刻が発生した（即ち有給や半休等を除いた）労働日数を数え上げる
        """
        your_work_counts = float(self.soup.find("div", class_="work_count").string)
        your_work_counts += holiday_counts
        return your_work_counts

    def get_work_hours(self) -> float:
        """
        ユーザーの前日までの総労働時間（「フレ労働時間」）を取得する
        """
        work_hours = self._clean_text(self.soup.find("td", class_="custom3").string)
        try:
            return float(work_hours)
        except ValueError:
            # 月初は前日までの勤務時間を取得できないので ValueError になる
            return 0.0

    def get_today_kintai(self) -> Tuple[str, str]:
        """
        ユーザーの当日の出勤打刻時間の取得と、8時間勤務した場合の退勤時間の計算を行う
        """
        start_time_string, teiji_time_string = "", ""
        try:
            st_string_dirty = self.soup.find_all("td", class_="start_end_timerecord specific-uncomplete")[
                -2
            ].text
            # 上記の出力例: '\n\n\nIC\n\n09:02\n\n'
            start_time_string = st_string_dirty.split(":")[0][-2:] + ":" + st_string_dirty.split(":")[1][:2]
            hhmm = start_time_string.split(":")
            teiji_time_string = ":".join([str(self._str_to_int(hhmm[0]) + (WORK_HOUR + 1)), hhmm[1]])
        except Exception:
            logger.info("打刻しましたか？退勤後なら問題ないですが")
        finally:
            return start_time_string, teiji_time_string

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
