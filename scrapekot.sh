#!/bin/sh
DIR=${HOME}/.scrape_kot
if [ ! -f "$DIR/config.py" ]; then
  DIR=${PWD}
fi

if [ "$1" == "notify" ] || [ "$1" == "console" ]; then
  echo $1
else
  echo "Error: you need one of the following arguments: 'notify' or 'console'"
  exit 1
fi

docker run -v "${DIR}/config.py":/scrape_kot/config.py -it --rm takaiyuk/scrape-kot run.py $1

