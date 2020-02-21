#!/bin/sh

if [ "$2" == "-y" ]; then
  python -m my_recorder.run --cmd "$1" --yes
else
  python -m my_recorder.run --cmd "$1"
fi
