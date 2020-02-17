#!/bin/sh

DIR=${HOME}/.scrape_kot
if [ ! -f "$DIR/config.py" ]; then
  DIR=${PWD}
fi

docker run -v "${DIR}/config.py":/scrape_kot/config.py -v my_recorder:/scrape_kot/my_recorder -it --rm takaiyuk/scrape-kot -m my_recorder.run -c "$1"
