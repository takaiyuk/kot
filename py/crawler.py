# Import
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


# Class
class Browser:
    def __init__(self, driver):
        self.driver = driver

    def _get_random(self, a=1, b=3):
        return random.uniform(a, b)

    def back(self):
        self.driver.back()

    def click(self, xpath):
        self.driver.find_element_by_xpath(xpath).click()

    def get(self, url):
        self.driver.get(url)
        ts = self._get_random(1, 1)
        time.sleep(ts)

    def save(self, filepath):
        html = self.driver.page_source
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)

    def scroll(self, height):
        self.driver.execute_script("window.scrollTo(0, " + str(height) + ");")

    def send(self, xpath, strings):
        self.driver.find_element_by_xpath(xpath).send_keys(strings)

    def source(self):
        return self.driver.page_source


class Crawler:
    def __init__(self, params):
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
                self.driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)
            else:
                self.driver = webdriver.Chrome(options=options)
        self.browser = Browser(self.driver)

    def get_source(self):
        # トップページ
        self.browser.get(TOP_URL)

        # ID/PASS 入力
        self.browser.send('//*[@id="login_id"]', YOUR_ID)
        self.browser.send('//*[@id="login_password"]', YOUR_PW)

        # ログイン
        self.browser.click('//*[@id="login_button"]')

        # ソースを取得
        page_source = self.browser.source()

        # プロセス消す
        self.driver.quit()

        return page_source
