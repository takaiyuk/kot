#!/bin/sh
DIR=${HOME}/.scrape_kot
if [ ! -f "$DIR/config.py" ]; then
  DIR=${PWD}
fi
echo $DIR
docker run -v "${DIR}/config.py":/scrape_kot/config.py -it --rm takaiyuk/scrape-kot run.py console

