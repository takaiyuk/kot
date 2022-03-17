import sys
import traceback
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from kot.aggregate import Aggregator
from kot.config import load_config
from kot.crawl import Browser, Crawler, DriverOptions
from kot.logger import logger
from kot.notify import Console, SlackClient
from kot.punch import MyRecorder, PunchParams
from kot.scrape import Scraper

FILEPATH = "./config.yaml"


@dataclass
class ScrapeKOTParams(DriverOptions):
    is_console: bool


@dataclass
class MyRecorderParams(DriverOptions):
    command: str
    message: str
    yes: bool
    is_debug: bool


def scrape_kot(params: ScrapeKOTParams) -> None:
    try:
        cfg = load_config(FILEPATH)
        driver_options = DriverOptions(
            is_amazon_linux=params.is_amazon_linux,
            is_chrome=params.is_chrome,
            is_chronium=params.is_chronium,
            is_firefox=params.is_firefox,
            is_headless=params.is_headless,
        )
        browser = Browser.build(driver_options)
        page_source = Crawler(browser).get_page_source(cfg)
        scraped_data = Scraper(page_source).extract()
        aggregated_data = Aggregator().aggregate(scraped_data)
        if params.is_console:
            Console.display(aggregated_data, datetime.today())
        else:
            SlackClient().notify(cfg, aggregated_data)
    except Exception as e:
        t, v, tb = sys.exc_info()
        x = traceback.format_exception(t, v, tb)
        raise Exception(f"{''.join(x)}" + str(e))


def punch_myrecorder(params: MyRecorderParams) -> None:
    try:
        cfg = load_config(FILEPATH)
        driver_options = DriverOptions(
            is_amazon_linux=params.is_amazon_linux,
            is_chrome=params.is_chrome,
            is_chronium=params.is_chronium,
            is_firefox=params.is_firefox,
            is_headless=params.is_headless,
        )
        punch_params = PunchParams(
            command=params.command,
            message=params.message,
            yes=params.yes,
            is_debug=params.is_debug,
        )
        browser = Browser.build(driver_options)
        MyRecorder(browser, punch_params).punch(cfg)
    except Exception as e:
        t, v, tb = sys.exc_info()
        x = traceback.format_exception(t, v, tb)
        raise Exception(f"{''.join(x)}" + str(e))


def lambda_handler(event: Any, context: Any) -> None:
    params = ScrapeKOTParams(
        is_amazon_linux=True,
        is_chrome=True,
        is_chronium=True,
        is_firefox=False,
        is_headless=True,
        is_console=True,
    )
    logger.info(params)
    scrape_kot(params)
