import sys
import traceback
from typing import Any

from kot.aggregate import Aggregator
from kot.config import load_config
from kot.crawl import Crawler, ScrapeKOTParams
from kot.logger import logger
from kot.notify import Console, SlackClient
from kot.punch import MyRecorder, MyRecorderParams
from kot.scrape import Scraper

FILEPATH = "./config.yaml"


def scrape_kot(params: ScrapeKOTParams) -> None:
    try:
        cfg = load_config(FILEPATH)
        page_source = Crawler(params).get_page_source(cfg)
        scraped_data = Scraper(page_source).extract()
        aggregated_data = Aggregator().aggregate(scraped_data)
        if params.is_console:
            Console.display(aggregated_data)
        else:
            SlackClient().notify(cfg, aggregated_data)
    except Exception as e:
        t, v, tb = sys.exc_info()
        x = traceback.format_exception(t, v, tb)
        logger.error(f"{''.join(x)}" + str(e))


def punch_myrecorder(params: MyRecorderParams) -> None:
    try:
        cfg = load_config(FILEPATH)
        MyRecorder(params).punch(cfg)
    except Exception as e:
        t, v, tb = sys.exc_info()
        x = traceback.format_exception(t, v, tb)
        logger.error(f"{''.join(x)}" + str(e))


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
