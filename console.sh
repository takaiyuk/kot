#!/bin/sh

docker run -v "${PWD}/config.py":/scrape_kot/config.py -v "${PWD}":/scrape_kot/drivers -it --rm takaiyuk/scrape-kot run.py console

