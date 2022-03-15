import random
import time
from dataclasses import dataclass
from typing import Union

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as GeckoService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.utils import ChromeType

from kot.config import Config

TOP_URL = "https://s3.kingtime.jp/admin"
DRIVER_PATH = "/tmp"


@dataclass
class DriverOptions:
    is_amazon_linux: bool
    is_chrome: bool
    is_chronium: bool
    is_firefox: bool
    is_headless: bool


@dataclass
class ScrapeKOTParams:
    is_amazon_linux: bool
    is_chrome: bool
    is_chronium: bool
    is_firefox: bool
    is_headless: bool
    is_console: bool


class Driver:
    @classmethod
    def build(
        cls, driver_options: DriverOptions
    ) -> Union[webdriver.Chrome, webdriver.Firefox]:
        options = webdriver.ChromeOptions()
        options = cls._set_default_chrome_options(options, driver_options)
        driver: Union[webdriver.Chrome, webdriver.Firefox]
        if driver_options.is_chrome:
            if driver_options.is_chronium:
                chrome_service = ChromeService(
                    ChromeDriverManager(
                        path=DRIVER_PATH, chrome_type=ChromeType.CHROMIUM
                    ).install()
                )
            else:
                chrome_service = ChromeService(
                    ChromeDriverManager(path=DRIVER_PATH).install()
                )
            driver = webdriver.Chrome(service=chrome_service, options=options)
        elif driver_options.is_firefox:
            gecko_service = GeckoService(GeckoDriverManager(path=DRIVER_PATH).install())
            driver = webdriver.Firefox(service=gecko_service, options=options)
        else:
            raise ValueError(
                "driver_options.is_chrome or driver_options.is_firefox must be True"
            )
        return driver

    @classmethod
    def _set_default_chrome_options(
        cls,
        options: webdriver.ChromeOptions,
        driver_options: DriverOptions,
    ) -> webdriver.ChromeOptions:
        if driver_options.is_headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280x1696")
        if driver_options.is_amazon_linux:
            options.add_argument("--disable-application-cache")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-infobars")
            options.add_argument("--hide-scrollbars")
            options.add_argument("--enable-logging")
            options.add_argument("--log-level=0")
            options.add_argument("--single-process")
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--homedir=/tmp")
        return options


class Browser:
    def __init__(self, driver: Union[webdriver.Chrome, webdriver.Firefox]) -> None:
        self.driver = driver

    def _get_random(self, a: int = 1, b: int = 3) -> float:
        return random.uniform(a, b)

    def back(self) -> None:
        self.driver.back()
        self.sleep()

    def click(self, xpath: str) -> None:
        self.driver.find_element_by_xpath(xpath).click()
        self.sleep()

    def get(self, url: str) -> None:
        # The `driver.get` method will navigate to a page given by the URL.
        self.driver.get(url)
        self.sleep()

    def quit(self) -> None:
        self.driver.quit()

    def save(self, filepath: str) -> None:
        html = self.driver.page_source
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)

    def scroll(self, height: int) -> None:
        self.driver.execute_script("window.scrollTo(0, " + str(height) + ");")

    def send(self, xpath: str, string: str) -> None:
        self.driver.find_element_by_xpath(xpath).send_keys(string)

    def sleep(self, a: int = 1, b: int = 2) -> None:
        ts = self._get_random(a, b)
        time.sleep(ts)

    @property
    def current_url(self) -> str:
        return self.driver.current_url

    @property
    def page_source(self) -> str:
        return self.driver.page_source


class Crawler:
    def __init__(self, params: ScrapeKOTParams) -> None:
        driver_options = DriverOptions(
            is_amazon_linux=params.is_amazon_linux,
            is_chrome=params.is_chrome,
            is_chronium=params.is_chronium,
            is_firefox=params.is_firefox,
            is_headless=params.is_headless,
        )
        driver = Driver.build(driver_options)
        self.browser = Browser(driver)

    def get_page_source(self, cfg: Config) -> str:
        try:
            # トップページ
            self.browser.get(TOP_URL)
            # ID/PASS 入力
            self.browser.send('//*[@id="login_id"]', cfg.account.id)
            self.browser.send('//*[@id="login_password"]', cfg.account.password)
            # ログイン
            self.browser.click('//*[@id="login_button"]')
            # ログイン成功したか確認
            url = self.browser.current_url
            if url == TOP_URL:
                raise Exception("login failed")
            # ソースを取得
            page_source = self.browser.page_source
        finally:
            # プロセス消す
            self.browser.quit()
        return page_source
