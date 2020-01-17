#!/bin/sh

docker run -v "${HOME}/.scrape_kot/config.py":/scrape_kot/config.py -it --rm takaiyuk/scrape-kot run.py console

