#!/bin/bash

CONFIG_PATH=${HOME}/.kot/config.yaml
if [ ! -f "$CONFIG_PATH" ]; then
  CONFIG_PATH=${PWD}/config.yaml
fi

if [ "$1" == "slack" ]; then
  CONSOLE="--no-console"
  echo ${CONSOLE}
elif [ "$1" == "" ] || [ "$1" == "console" ]; then
  CONSOLE="--console"
  echo ${CONSOLE}
else
  echo "Error: you need one of the following arguments: '', 'slack' or 'console'"
  exit 1
fi

docker compose run --rm app kot scrape ${CONSOLE} --browser-kind remote
