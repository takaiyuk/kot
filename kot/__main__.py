import typer

from kot.common.logger import logger
from kot.service import (
    MyRecorderParams,
    ScrapeKOTParams,
    InitializeParams,
    punch_myrecorder,
    scrape_kot,
    initialize_dirver,
)

app = typer.Typer(add_completion=False)


@app.command()
def scrape(
    amazon_linux: bool = False,
    chrome: bool = True,
    chromium: bool = False,
    firefox: bool = False,
    headless: bool = True,
    console: bool = True,
) -> None:
    params = ScrapeKOTParams(
        is_amazon_linux=amazon_linux,
        is_chrome=chrome,
        is_chromium=chromium,
        is_firefox=firefox,
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
    chrome: bool = True,
    chromium: bool = False,
    firefox: bool = False,
    headless: bool = True,
) -> None:
    params = MyRecorderParams(
        is_amazon_linux=amazon_linux,
        is_chrome=chrome,
        is_chromium=chromium,
        is_firefox=firefox,
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
        is_chrome=True,
        is_chromium=True,
        is_firefox=False,
        is_headless=True,
    )
    logger.info(params)
    initialize_dirver(params)


if __name__ == "__main__":
    app()
