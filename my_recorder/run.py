# Import
import argparse
import json
import os
import random
import requests
from selenium import webdriver
import time

from config import (
    YOUR_ID,
    YOUR_PW,
)
from my_recorder.const import (
    DRIVER_PATH,
    TOP_URL,
    CMD_DICT,
    CMD_NAME_DICT,
    CMD_MESSAGE_DICT,
)


parser = argparse.ArgumentParser("parser of command that define which botton to click")
parser.add_argument(
    "--cmd",
    type=str,
    required=True,
    choices=["start", "end", "rest-start", "rest-end"],
    help="command",
)
parser.add_argument("--message", type=str, required=False, help="message to notify")
parser.add_argument("--yes", action="store_true", help="yes option")
arguments = parser.parse_args()
cmd = vars(arguments)["cmd"]
message = vars(arguments)["message"]
yes = vars(arguments)["yes"]


class Browser:
    def __init__(self, driver: webdriver.Chrome) -> None:
        self.driver = driver

    def _get_random(self, a: int = 1, b: int = 3) -> float:
        return random.uniform(a, b)

    def back(self) -> None:
        self.driver.back()

    def click(self, xpath: str) -> None:
        self.driver.find_element_by_xpath(xpath).click()

    def get(self, url: str) -> None:
        self.driver.get(url)
        ts = self._get_random(2, 3)
        time.sleep(ts)

    def get_url(self) -> str:
        return self.driver.current_url

    def save(self, filepath: str) -> None:
        html = self.driver.page_source
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)

    def scroll(self, height: int) -> None:
        self.driver.execute_script("window.scrollTo(0, " + str(height) + ");")

    def send(self, xpath: str, string: str) -> None:
        self.driver.find_element_by_xpath(xpath).send_keys(string)

    def source(self) -> str:
        return self.driver.page_source


class Driver:
    def __init__(self, params: argparse.Namespace = None) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280x1696")
        if os.path.exists(DRIVER_PATH):
            self.driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)
        else:
            self.driver = webdriver.Chrome(options=options)


class Puncher:
    def __init__(self, params: argparse.Namespace = None) -> None:
        self.driver = Driver(params).driver
        self.browser = Browser(self.driver)

    def click(self) -> None:
        # トップページ
        self.browser.get(TOP_URL)

        # ID/PASS 入力
        self.browser.send('//*[@id="id"]', YOUR_ID)
        self.browser.send('//*[@id="password"]', YOUR_PW)

        # ログイン
        self.browser.click('//*[@id="modal_window"]/div/div/div[3]/div/div')

        # TODO: ログイン成功したか確認
        # 何かしらの方法で確認する：ヘッドレスにせず目視...?
        # 成功時もURLの遷移なし・失敗時もモーダルが出るだけなのでseleniumでのログインの成否判断が難しい

        # 確認する
        if yes:
            val = "y"
            time.sleep(3)
        else:
            val = input(f"{CMD_NAME_DICT[cmd]}ボタンを押していいですか？[y/n]: ")
        # 実行する
        if val != "y":
            print(f"{CMD_NAME_DICT[cmd]}ボタンはスキップしました")
        else:
            assert cmd in CMD_DICT.keys()
            xpath = CMD_DICT[cmd]
            self.browser.click(xpath)
            print(f"{CMD_NAME_DICT[cmd]}ボタンが押されました（多分）")

        # プロセス消す
        self.driver.quit()

    def notify(self) -> None:
        from config import (
            MYRECORDER_WEBHOOK_URL,
            MYRECORDER_NOTIFY_CHANNEL,
        )

        if message is None:
            kintai_message = CMD_MESSAGE_DICT[cmd]
        else:
            kintai_message = message
        requests.post(
            MYRECORDER_WEBHOOK_URL,
            data=json.dumps(
                {
                    "channel": MYRECORDER_NOTIFY_CHANNEL,
                    "attachments": [{"pretext": f"{kintai_message}"}],
                }
            ),
        )

    def run(self) -> None:
        self.click()
        try:
            self.notify()
        except ImportError:
            pass


if __name__ == "__main__":
    Puncher().run()
