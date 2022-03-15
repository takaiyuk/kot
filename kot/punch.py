import json
import random
from dataclasses import dataclass

import requests

from kot.config import Config
from kot.crawl import Browser, Driver, DriverOptions
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
class MyRecorderParams:
    is_amazon_linux: bool
    is_chrome: bool
    is_chronium: bool
    is_firefox: bool
    is_headless: bool
    command: str
    message: str
    yes: bool
    is_debug: bool


class MyRecorder:
    def __init__(self, params: MyRecorderParams) -> None:
        driver_options = DriverOptions(
            is_amazon_linux=params.is_amazon_linux,
            is_chrome=params.is_chrome,
            is_chronium=params.is_chronium,
            is_firefox=params.is_firefox,
            is_headless=params.is_headless,
        )
        driver = Driver.build(driver_options)
        self.browser = Browser(driver)
        self.params = params

    def punch(self, cfg: Config) -> None:
        self.click(cfg)
        self.notify(cfg)

    def click(self, cfg: Config) -> None:
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
            cmd = self.params.command
            yes = self.params.yes
            is_debug = self.params.is_debug
            myrecoder_option = getattr(MyRecorderOptions, cmd)
            # 確認する
            if yes:
                val = "y"
                self.browser.sleep()
            else:
                val = input(f"{myrecoder_option.name}ボタンを押していいですか？[y/n]: ")
            # 実行する
            if val != "y":
                logger.info(f"{myrecoder_option.name}ボタンはスキップしました")
            else:
                assert cmd in MyRecorderOptions.__annotations__.keys()
                xpath = myrecoder_option.xpath
                if not is_debug:
                    raise ValueError  # FIXME: 開発中に誤ってボタンを押してしまわないように例外を発生させている
                    self.browser.click(xpath)
                    logger.info(f"{myrecoder_option.name}ボタンが押されました（多分）")
                else:
                    logger.info(f"{myrecoder_option.name}ボタンは押されない")
        finally:
            # プロセス消す
            self.browser.quit()

    def notify(self, cfg: Config) -> None:
        cmd = self.params.command
        message = self.params.message
        is_debug = self.params.is_debug
        if message is None or message == "":
            kintai_messages = getattr(MyRecorderOptions, cmd).messages
            idx = random.randint(0, len(kintai_messages) - 1)
            kintai_message = kintai_messages[idx]
        else:
            kintai_message = message
        if not is_debug:
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
