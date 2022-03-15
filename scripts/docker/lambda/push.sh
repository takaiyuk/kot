#!/bin/sh

source $PWD/scripts/docker/lambda/.env

aws ecr get-login-password | docker login --username AWS --password-stdin $ECR_URI
docker tag $IMAGE:$TAG $ECR_URI/$IMAGE:$TAG
docker push $ECR_URI/$IMAGE:$TAG
