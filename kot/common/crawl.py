import random
import time
from dataclasses import dataclass
from typing import Any, Optional, Type, TypeVar, Union

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as GeckoService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.utils import ChromeType

TOP_URL = "https://s3.kingtime.jp/admin"
DRIVER_PATH = "/tmp"
B = TypeVar("B", bound="Browser")


@dataclass
class DriverOptions:
    is_amazon_linux: bool
    is_chrome: bool
    is_chronium: bool
    is_firefox: bool
    is_headless: bool


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
        self.driver.find_element_by_xpath(xpath).click()
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


class BaseCrawler:
    def __init__(self, browser: B) -> None:
        self.browser = browser

    def run(self, params: Any) -> Any:
        raise NotImplementedError
