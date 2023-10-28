#!/bin/sh
source ./scripts/docker/lambda/.env

# NOTE: --platform linux/x86_64 is required for chromium to work
docker build -f ./docker/lambda/Dockerfile -t $IMAGE:$TAG --platform linux/x86_64 .
