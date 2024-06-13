#!/bin/bash

PROJECT_NAME=whisper-api
VERSION=v0.1.0

IMAGE_NAME=${PROJECT_NAME}:${VERSION}

docker login
docker build --build-arg MODEL=small -t $IMAGE_NAME .
docker tag $IMAGE_NAME vonsovsky/$IMAGE_NAME
docker push vonsovsky/$IMAGE_NAME