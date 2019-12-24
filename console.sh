#!/bin/sh

docker run -v "${PWD}/config.py":/scrape_kot/config.py -it --rm takaiyuk/scrape-kot run.py console

