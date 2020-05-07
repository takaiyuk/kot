#!/bin/sh

if [ "$2" == "-y" ] && [ "$3" != "" ]; then
  python -m my_recorder.run --cmd "$1" --yes --message "$3"
elif [ "$2" == "-y" ]; then
  python -m my_recorder.run --cmd "$1" --yes
elif [ "$2" != "" ]; then
  python -m my_recorder.run --cmd "$1" --message "$2"
else
  python -m my_recorder.run --cmd "$1"
fi
