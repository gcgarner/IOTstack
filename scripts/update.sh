#!/bin/bash

# should not run as root
[ "$EUID" -eq 0 ] && echo "This script should NOT be run using sudo" && exit -1

echo "Stopping containers"
docker-compose down

echo "Downloading latest images from docker hub ... this can take a long time"
docker-compose pull

echo "Building images if needed"
docker-compose build

echo "Starting stack up again"
docker-compose up -d

echo "Consider running prune-images to free up space"

