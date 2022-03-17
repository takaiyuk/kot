import json
import random
from dataclasses import dataclass

import requests

from kot.config import Config
from kot.crawl import Browser
from kot.logger import logger

TOP_URL = "https://s3.kingtime.jp/independent/recorder/personal/"


@dataclass
class Cmd:
    xpath: str
    name: str
    messages: list[str]


@dataclass
class MyRecorderOptions:
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


@dataclass
class PunchParams:
    command: str
    message: str
    yes: bool
    is_debug: bool


class MyRecorder:
    def __init__(self, browser: Browser, params: PunchParams) -> None:
        self.browser = browser
        self.cmd = params.command
        self.message = params.message
        self.yes = params.yes
        self.is_debug = params.is_debug

    def punch(self, cfg: Config) -> None:
        self._punch(cfg)
        self._notify(cfg)

    def _punch(self, cfg: Config) -> None:
        try:
            # トップページ
            self.browser.get(TOP_URL)
            # ID/PASS 入力
            self.browser.send('//*[@id="id"]', cfg.account.id)
            self.browser.send('//*[@id="password"]', cfg.account.password)
            # ログイン
            self.browser.click('//*[@id="modal_window"]/div/div/div[3]/div/div')
            """
            # TODO: ログイン成功したか確認
            # 成功時もURLの遷移なし・失敗時もモーダルが出るだけなのでseleniumでのログインの成否判断が難しい
            """
            myrecoder_option = getattr(MyRecorderOptions, self.cmd)
            # 確認する
            if self.yes:
                val = "y"
                self.browser.sleep()
            else:
                val = input(f"{myrecoder_option.name}ボタンを押していいですか？[y/n]: ")
            # 実行する
            if val != "y":
                logger.info(f"{myrecoder_option.name}ボタンはスキップしました")
            else:
                assert self.cmd in MyRecorderOptions.__annotations__.keys()
                xpath = myrecoder_option.xpath
                if not self.is_debug:
                    raise ValueError  # FIXME: 開発中に誤ってボタンを押してしまわないように例外を発生させている
                    self.browser.click(xpath)
                    logger.info(f"{myrecoder_option.name}ボタンが押されました（多分）")
                else:
                    logger.info(f"{myrecoder_option.name}ボタンは押されない")
        finally:
            # プロセス消す
            self.browser.quit()

    def _notify(self, cfg: Config) -> None:
        if self.message is None or self.message == "":
            kintai_messages = getattr(MyRecorderOptions, self.cmd).messages
            idx = random.randint(0, len(kintai_messages) - 1)
            kintai_message = kintai_messages[idx]
        else:
            kintai_message = self.message
        if not self.is_debug:
            raise ValueError  # FIXME: 開発中に誤ってSlackに投稿されてしまわないように例外を発生させている
            self._post_slack(cfg, kintai_message)
            logger.info(f"通知されるメッセージ: {kintai_message}")
        else:
            logger.info(f"通知されないメッセージ: {kintai_message}")

    def _post_slack(self, cfg: Config, message: str) -> None:
        requests.post(
            cfg.myrecorder.slack.webhook_url,
            data=json.dumps(
                {
                    "username": cfg.myrecorder.slack.username,
                    "icon_emoji": cfg.myrecorder.slack.icon_emoji,
                    "channel": cfg.myrecorder.slack.channel,
                    "text": message,
                }
            ),
        )
