#!/bin/sh
source ./scripts/docker/lambda/.env

docker build -f ./docker/lambda/Dockerfile -t $IMAGE:$TAG .
