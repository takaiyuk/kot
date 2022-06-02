import typer

from kot.common.logger import logger
from kot.service import MyRecorderParams, ScrapeKOTParams, punch_myrecorder, scrape_kot

app = typer.Typer(add_completion=False)


@app.command()
def scrape(
    amazon_linux: bool = False,
    chrome: bool = True,
    chronium: bool = False,
    firefox: bool = False,
    headless: bool = True,
    console: bool = True,
) -> None:
    params = ScrapeKOTParams(
        is_amazon_linux=amazon_linux,
        is_chrome=chrome,
        is_chronium=chronium,
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
    chronium: bool = False,
    firefox: bool = False,
    headless: bool = True,
) -> None:
    params = MyRecorderParams(
        is_amazon_linux=amazon_linux,
        is_chrome=chrome,
        is_chronium=chronium,
        is_firefox=firefox,
        is_headless=headless,
        command=command,
        message=message,
        yes=yes,
        is_debug=debug,
    )
    logger.info(params)
    punch_myrecorder(params)


if __name__ == "__main__":
    app()
