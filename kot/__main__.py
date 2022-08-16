import typer

from kot.common.crawl import BrowserKind
from kot.common.logger import logger
from kot.service import (
    InitializeParams,
    MyRecorderParams,
    ScrapeKOTParams,
    initialize_dirver,
    punch_myrecorder,
    scrape_kot,
)

app = typer.Typer(add_completion=False)


@app.command()
def scrape(
    console: bool = True,
    amazon_linux: bool = False,
    browser_kind: BrowserKind = BrowserKind.chrome,
    headless: bool = True,
) -> None:
    params = ScrapeKOTParams(
        is_amazon_linux=amazon_linux,
        browser_kind=browser_kind,
        is_headless=headless,
        is_console=console,
    )
    logger.info(params)
    scrape_kot(params)


@app.command()
def myrecorder(
    command: str,
    yes: bool = False,
    message: str = "",
    debug: bool = False,
    amazon_linux: bool = False,
    browser_kind: BrowserKind = BrowserKind.chrome,
    headless: bool = True,
) -> None:
    params = MyRecorderParams(
        is_amazon_linux=amazon_linux,
        browser_kind=browser_kind,
        is_headless=headless,
        command=command,
        message=message,
        yes=yes,
        is_debug=debug,
    )
    logger.info(params)
    punch_myrecorder(params)


@app.command()
def initialize() -> None:
    """
    Get cache of the latest chromedriver version for chromium in kot docker image
    """
    params = InitializeParams(
        is_amazon_linux=False,
        browser_kind=BrowserKind.chromium,
        is_headless=True,
    )
    logger.info(params)
    initialize_dirver(params)


if __name__ == "__main__":
    app()
