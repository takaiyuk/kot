#!/bin/sh

DIR=${HOME}/.scrape_kot
if [ ! -f "$DIR/config.py" ]; then
  DIR=${PWD}
fi

if [ "$2" == "-y" ] && [ "$3" != "" ]; then
  docker run -v "${DIR}/config.py":/scrape_kot/config.py -it --rm takaiyuk/scrape-kot -m my_recorder.run --cmd "$1" --yes --message "$3"
elif [ "$2" == "-y" ]; then
  docker run -v "${DIR}/config.py":/scrape_kot/config.py -it --rm takaiyuk/scrape-kot -m my_recorder.run --cmd "$1" --yes
elif [ "$2" != "" ]; then
  docker run -v "${DIR}/config.py":/scrape_kot/config.py -it --rm takaiyuk/scrape-kot -m my_recorder.run --cmd "$1" --message "$2"
else
  docker run -v "${DIR}/config.py":/scrape_kot/config.py -it --rm takaiyuk/scrape-kot -m my_recorder.run --cmd "$1"
fi
