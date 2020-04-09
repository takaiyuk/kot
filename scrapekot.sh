#!/bin/sh
DIR=${HOME}/.scrape_kot
if [ ! -f "$DIR/config.py" ]; then
  DIR=${PWD}
fi

SUBCMD="notify"
if [ "$1" == "" ] || [ "$1" == "notify" ]; then
  echo ${SUBCMD}
elif [ "$1" == "console" ]; then
  SUBCMD="console"
  echo ${SUBCMD}
else
  echo "Error: you need one of the following arguments: '', 'notify' or 'console'"
  exit 1
fi

docker run -v "${DIR}/config.py":/scrape_kot/config.py -it --rm takaiyuk/scrape-kot run.py ${SUBCMD}
