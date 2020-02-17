TOP_URL = "https://s3.kingtime.jp/independent/recorder/personal/"
DRIVER_PATH = "./drivers/chromedriver"
CMD_DICT = {
    "start": '//*[@id="record_qmXXCxw9WEWN3X/YrkMWuQ=="]/div/div[2]',  # 出勤
    "end": '//*[@id="record_j8ekmJaw6W3M4w3i6hlSIQ=="]/div/div[2]',  # 退勤
    "rest-start": '//*[@id="record_tgI75YcXVUW7d/VjiooYtA=="]/div/div',  # 休憩開始
    "rest-end": '//*[@id="record_1HnBUiZe8JiePXoZZkorfw=="]/div/div',  # 休憩終了
}
CMD_NAME_DICT = {
    "start": "出勤",
    "end": "退勤",
    "rest-start": "休憩開始",
    "rest-end": "休憩終了",
}
