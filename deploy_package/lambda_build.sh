#!/bin/sh

docker build -t scrape-kot-lambda .
docker run -v "${PWD}":/var/task -it --rm scrape-kot-lambda
