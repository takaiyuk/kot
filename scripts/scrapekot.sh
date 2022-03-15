#!/bin/bash

CONFIG_PATH=${HOME}/.kot/config.yaml
if [ ! -f "$CONFIG_PATH" ]; then
  CONFIG_PATH=${PWD}/config.yaml
fi

if [ "$1" == "notify" ]; then
  CONSOLE="--no-console"
  echo ${CONSOLE}
elif [ "$1" == "" ] || [ "$1" == "console" ]; then
  CONSOLE="--console"
  echo ${CONSOLE}
else
  echo "Error: you need one of the following arguments: '', 'notify' or 'console'"
  exit 1
fi

docker run --rm -v ${CONFIG_PATH}:/kot/config.yaml takaiyuk/kot -m kot scrape ${CONSOLE} --chronium
