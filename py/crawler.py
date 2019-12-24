# Import
import argparse
import random
from selenium import webdriver
import time
import os

from config import YOUR_ID, YOUR_PW
from .const import (
    DRIVER_PATH,
    TOP_URL,
    AMAZONLINUX_CHROME_PATH,
    AMAZONLINUX_DRIVER_PATH,
)


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
    def __init__(self, params: argparse.Namespace) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        if params.lambda_deploy is True:
            options.binary_location = AMAZONLINUX_CHROME_PATH
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1280x1696")
            options.add_argument("--disable-application-cache")
            options.add_argument("--disable-infobars")
            options.add_argument("--no-sandbox")
            options.add_argument("--hide-scrollbars")
            options.add_argument("--enable-logging")
            options.add_argument("--log-level=0")
            options.add_argument("--single-process")
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--homedir=/tmp")
            self.driver = webdriver.Chrome(
                executable_path=AMAZONLINUX_DRIVER_PATH, options=options
            )
        else:
            if os.path.exists(DRIVER_PATH):
                self.driver = webdriver.Chrome(
                    executable_path=DRIVER_PATH, options=options
                )
            else:
                self.driver = webdriver.Chrome(options=options)


class Crawler:
    def __init__(self, params: argparse.Namespace) -> None:
        self.driver = Driver(params).driver
        self.browser = Browser(self.driver)

    def get_source(self) -> str:
        # トップページ
        self.browser.get(TOP_URL)

        # ID/PASS 入力
        self.browser.send('//*[@id="login_id"]', YOUR_ID)
        self.browser.send('//*[@id="login_password"]', YOUR_PW)

        # ログイン
        self.browser.click('//*[@id="login_button"]')

        # ログイン成功したか確認
        url = self.browser.get_url()
        if url == TOP_URL:
            raise Exception("login failed")

        # ソースを取得
        page_source = self.browser.source()

        # プロセス消す
        self.driver.quit()

        return page_source
