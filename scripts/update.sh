#!/bin/bash

echo "Stopping containers"
docker-compose down

echo "Downloading latest images from docker hub ... this can take a long time"
docker-compose pull

echo "Building images if needed"
docker-compose build

echo "Starting stack up again"
docker-compose up -d

echo "Consider running prune-images to free up space"
