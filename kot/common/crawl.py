import os
import random
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Type, TypeVar, Union

import boto3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as GeckoService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from webdriver_manager.firefox import GeckoDriverManager

TOP_URL = "https://s3.kingtime.jp/admin"
DRIVER_PATH = "/tmp"
_S3_CACHE_DIR = os.path.join(os.getenv("S3_CACHE_BUCKET", ""), "wdm/drivers/chromedriver/linux64")
DRIVER_VERSION = os.getenv("DRIVER_VERSION", "")
S3_CACHE_PATH = os.path.join(_S3_CACHE_DIR, DRIVER_VERSION, "chromedriver")
B = TypeVar("B", bound="Browser")


class BrowserKind(str, Enum):
    chrome = "chrome"
    chromium = "chromium"
    firefox = "firefox"


@dataclass
class DriverOptions:
    is_amazon_linux: bool
    browser_kind: BrowserKind
    is_headless: bool


class Driver:
    @classmethod
    def build(cls, driver_options: DriverOptions) -> Union[webdriver.Chrome, webdriver.Firefox]:
        browser_options = cls._get_browser_options(driver_options)
        """
        NOTE:
            * cache の確認
                * S3 に cache があればそれを DRIVER_PATH にダウンロードする
                    * set_cache_flag を下げる
                * cache がなければ何もしない
                    * set_cache_flag を立てる
            * cls._get_driver を実行
            * cache を S3 に保存する
                * set_cache_flag が立っていれば S3 に保存する
                * set_cache_flag が立っていなければ何もしない

        s3: $S3_CACHE_PATH/chromedriver
        local: $DRIVER_PATH/.wdm/drivers/chromedriver/linux64/$DRIVER_VERSION/chromedriver
        """
        driver_save_path = os.path.join(
            DRIVER_PATH, ".wdm/drivers/chromedriver/linux64", DRIVER_VERSION, "chromedriver"
        )
        set_cache_flag = True
        # cache が存在しているかつ、Lambda で実行時に cache を利用する。set_cache_flag は False にする。
        if check_s3_path_exists(S3_CACHE_PATH) and os.getenv("LAMBDA_TASK_ROOT"):
            cls.download_driver(S3_CACHE_PATH, driver_save_path)
            set_cache_flag = False
        driver = cls._get_driver(driver_options, browser_options)
        # set_cache_flag が True かつ、Lambda で実行時に cache を保存する。
        if set_cache_flag and os.getenv("LAMBDA_TASK_ROOT"):
            cls.upload_driver(driver_save_path, S3_CACHE_PATH)
        return driver

    @classmethod
    def _get_browser_options(
        cls, driver_options: DriverOptions
    ) -> Union[webdriver.ChromeOptions, webdriver.FirefoxOptions]:
        options: Union[webdriver.ChromeOptions, webdriver.FirefoxOptions]
        if (
            driver_options.browser_kind == BrowserKind.chrome
            or driver_options.browser_kind == BrowserKind.chromium
        ):
            options = webdriver.ChromeOptions()
        elif driver_options.browser_kind == BrowserKind.firefox:
            options = webdriver.FirefoxOptions()
        else:
            raise ValueError("driver_options.browser_kind must be one of chrome, chromium or firefox")

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

    @classmethod
    def _get_driver(
        cls,
        driver_options: DriverOptions,
        options: Union[webdriver.ChromeOptions, webdriver.FirefoxOptions],
    ):
        driver: Union[webdriver.Chrome, webdriver.Firefox]
        if (
            driver_options.browser_kind == BrowserKind.chrome
            or driver_options.browser_kind == BrowserKind.chromium
        ) and isinstance(options, webdriver.ChromeOptions):
            if driver_options.browser_kind == BrowserKind.chromium:
                chrome_service = ChromeService(
                    ChromeDriverManager(path=DRIVER_PATH, chrome_type=ChromeType.CHROMIUM).install()
                )
            else:
                chrome_service = ChromeService(ChromeDriverManager(path=DRIVER_PATH).install())
            driver = webdriver.Chrome(service=chrome_service, options=options)
        elif driver_options.browser_kind == BrowserKind.firefox and isinstance(
            options, webdriver.FirefoxOptions
        ):
            gecko_service = GeckoService(GeckoDriverManager(path=DRIVER_PATH).install())
            driver = webdriver.Firefox(service=gecko_service, options=options)
        else:
            raise ValueError(
                f"driver_options.browser_kind must be one of chrome, chromium or firefox: {driver_options.browser_kind}\n"
                f"or options must be consistent with browser_kind: {options}"
            )
        return driver

    @classmethod
    def download_driver(cls, s3_path: str, local_path: str) -> None:
        bucket = s3_path.split("/")[0]
        key = s3_path.split("/")[1:]
        s3 = boto3.client("s3")
        s3.download_file(bucket, key, local_path)

    @classmethod
    def upload_driver(cls, local_path: str, s3_path: str) -> None:
        bucket = s3_path.split("/")[0]
        key = s3_path.split("/")[1:]
        s3_client = boto3.client("s3")
        s3_client.upload_file(local_path, bucket, key)


class Browser:
    def __init__(self, driver: Union[webdriver.Chrome, webdriver.Firefox]) -> None:
        self.driver = driver

    @classmethod
    def build(cls: Type[B], driver_options: DriverOptions) -> B:
        driver = Driver.build(driver_options)
        return cls(driver)

    def _get_random(self, a: int = 1, b: int = 3) -> float:
        return random.uniform(a, b)

    def back(self) -> None:
        self.driver.back()
        self.sleep()

    def click(self, xpath: str) -> None:
        self.driver.find_element(by=By.XPATH, value=xpath).click()
        self.sleep()

    def get(self, url: str) -> None:
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
        self.driver.find_element(by=By.XPATH, value=xpath).send_keys(string)

    def sleep(self, a: int = 1, b: int = 2) -> None:
        ts = self._get_random(a, b)
        time.sleep(ts)

    @property
    def current_url(self) -> str:
        return self.driver.current_url

    @property
    def page_source(self) -> str:
        return self.driver.page_source


class BaseCrawler:
    def __init__(self, browser: B) -> None:
        self.browser = browser

    def run(self, params: Any) -> Any:
        raise NotImplementedError


def check_s3_path_exists(path: str) -> bool:
    bucket = path.split("/")[0]
    key = path.split("/")[1:]

    client = boto3.client("s3")
    result = client.list_objects(Bucket=bucket, Prefix=key)
    if "Contents" in result:
        return True
    else:
        return False
