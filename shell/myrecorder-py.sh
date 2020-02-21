#!/bin/sh

if [ "$2" == "-y" ]; then
  python -m my_recorder.run -c "$1" "$2"
else
  python -m my_recorder.run -c "$1"
fi
