# Import
import random
from selenium import webdriver
import time

from config import YOUR_ID, YOUR_PW
from .const import DRIVER_PATH, TOP_URL


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
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)
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
