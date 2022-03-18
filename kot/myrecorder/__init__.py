from dataclasses import dataclass


@dataclass
class MyRecorderOptions:
    @dataclass
    class Cmd:
        xpath: str
        name: str
        messages: list[str]

    start: Cmd = Cmd(
        xpath='//*[@id="record_qmXXCxw9WEWN3X/YrkMWuQ=="]/div/div[2]',
        name="出勤",
        messages=[":shukkin:", "業務開始します", "業務開始します！"],
    )
    end: Cmd = Cmd(
        xpath='//*[@id="record_j8ekmJaw6W3M4w3i6hlSIQ=="]/div/div[2]',
        name="退勤",
        messages=[
            ":taikin:",
            ":taikin::shimasu:",
            ":taikin::simasu:",
            ":taikin::shimashita:",
            "退勤します",
            "退勤します！",
        ],
    )
    rest_start: Cmd = Cmd(
        xpath='//*[@id="record_tgI75YcXVUW7d/VjiooYtA=="]/div/div',
        name="休憩開始",
        messages=[":kyuu::hajime:"],
    )
    rest_end: Cmd = Cmd(
        xpath='//*[@id="record_1HnBUiZe8JiePXoZZkorfw=="]/div/div',
        name="休憩終了",
        messages=[":kyuu::owari:"],
    )
