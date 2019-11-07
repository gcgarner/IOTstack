#!/bin/bash

pushd ~/IOTstack

[ -d ./backups ] || mkdir ./backups

#create the list of files to backup
echo "./docker-compose.yml" > list.txt
echo "./services/" >> list.txt
echo "./volumes/" >> list.txt

#if influxdb folder exists then back it up
if [ -d ./volumes/influxdb ];
then
    ./scripts/backup_influxdb.sh
    echo "./backups/influxdb/" >> list.txt
fi

echo "compressing stack folders"
sudo tar -czf \
./backups/docker.tar.gz \
--exclude=./volumes/influxdb/* \
-T list.txt

rm list.txt

echo "backup saved to ./backups/docker.tar.gz"

du -h ./backups/docker.tar.gz

if [ -f ./backups/dropbox ];
then
    echo "uploading to dropbox"
    ~/Dropbox-Uploader/dropbox_uploader.sh upload ~/IOTstack/backups/docker.tar.gz /IOTstackBU/
fi

if [ -f ./backups/rclone ];
then
    echo "uploading to Google Drive"
    rclone -P copy ./backups/docker.tar.gz gdrive:/IOTstackBU/
fi

popd
