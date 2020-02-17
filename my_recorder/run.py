# Import
import argparse
import os
import random
from selenium import webdriver
import time

from config import YOUR_ID, YOUR_PW
from my_recorder.const import (
    DRIVER_PATH,
    TOP_URL,
    CMD_DICT,
    CMD_NAME_DICT,
)


parser = argparse.ArgumentParser("parser of command that define which botton to click")
parser.add_argument(
    "-c",
    type=str,
    required=True,
    choices=["start", "end", "rest-start", "rest-end"],
    help="command",
)
ns = parser.parse_args()
cmd = vars(ns)["c"]


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
        ts = self._get_random(1, 1)
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
        # options.add_argument("--headless")
        options.add_argument("--no-sandbox")
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

        # 実行する
        val = input(f"{CMD_NAME_DICT[cmd]}ボタンを押していいですか？[y/n]: ")
        if val != "y":
            print(f"{CMD_NAME_DICT[cmd]}ボタンはスキップしました")
        else:
            assert cmd in CMD_DICT.keys()
            xpath = CMD_DICT[cmd]
            self.browser.click(xpath)
            print(f"{CMD_NAME_DICT[cmd]}ボタンが押されました（多分）")

        # プロセス消す
        self.driver.quit()

        return


if __name__ == "__main__":
    Puncher().click()
