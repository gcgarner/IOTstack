#!/bin/bash

pushd ~/IOTstack

[ -d ./backups ] || mkdir ./backups

./scripts/backup_influxdb.sh

echo "compressing stack folders"
sudo tar -czf \
./backups/docker.tar.gz \
--exclude=./volumes/influxdb/* \
./docker-compose.yml \
./services/ \
./volumes/ \
./backups/influxdb
echo "backup saved to ./backups/docker.tar.gz"

#cp ~/IOTstack/backups/docker.tar.gz ~
#echo "uploading to dropbox"
#~/Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/docker.tar.gz /IOTstackBU/
#rm /home/pi/docker.tar.gz


popd
