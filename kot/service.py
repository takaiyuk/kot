import sys
import traceback
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from kot.common.config import load_config
from kot.common.crawl import Browser, DriverOptions
from kot.common.logger import logger
from kot.myrecorder.crawl import Crawler as MyRecorderCrawler
from kot.myrecorder.crawl import CrawlerParams as MyRecorderCrawlerParams
from kot.myrecorder.notify import SlackClient as MyRecorderSlackClient
from kot.myrecorder.notify import SlackClientParams as MyRecorderSlackClientParams
from kot.scrapekot.aggregate import Aggregator
from kot.scrapekot.crawl import Crawler as ScrapeKOTCrawler
from kot.scrapekot.crawl import CrawlerParams as ScrapeKOTCrawlerParams
from kot.scrapekot.notify import Console
from kot.scrapekot.notify import SlackClient as ScrapeKOTSlackClient
from kot.scrapekot.notify import SlackClientParams as ScrapeKOTSlackClientParams
from kot.scrapekot.scrape import Scraper

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
        crawler_params = ScrapeKOTCrawlerParams(
            account_id=cfg.account.id,
            account_password=cfg.account.password,
        )
        slack_client_params = ScrapeKOTSlackClientParams(
            slack_webhook_url=cfg.scrapekot.slack.webhook_url,
            slack_channel=cfg.scrapekot.slack.channel,
            slack_icon_emoji=cfg.scrapekot.slack.icon_emoji,
            slack_username=cfg.scrapekot.slack.username,
            dt_now=datetime.now(),
        )
        browser = Browser.build(driver_options)
        crawled_data = ScrapeKOTCrawler(browser).run(crawler_params)
        scraped_data = Scraper(crawled_data).extract()
        aggregated_data = Aggregator().aggregate(scraped_data)
        if params.is_console:
            Console.display(aggregated_data, datetime.today())
        else:
            ScrapeKOTSlackClient().notify(slack_client_params, aggregated_data)
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
        crawler_params = MyRecorderCrawlerParams(
            account_id=cfg.account.id,
            account_password=cfg.account.password,
            command=params.command,
            message=params.message,
            yes=params.yes,
            is_debug=params.is_debug,
        )
        slack_client_params = MyRecorderSlackClientParams(
            slack_webhook_url=cfg.myrecorder.slack.webhook_url,
            slack_channel=cfg.myrecorder.slack.channel,
            slack_icon_emoji=cfg.myrecorder.slack.icon_emoji,
            slack_username=cfg.myrecorder.slack.username,
            command=params.command,
            message=params.message,
            yes=params.yes,
            is_debug=params.is_debug,
        )
        browser = Browser.build(driver_options)
        MyRecorderCrawler(browser).run(crawler_params)
        MyRecorderSlackClient().notify(slack_client_params)
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
