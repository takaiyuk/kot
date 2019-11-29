#!/bin/sh

docker run -v "${PWD}":/scrape_kot -v "${PWD}":/scrape_kot/drivers -it --rm takaiyuk/scrape-kot run.py

