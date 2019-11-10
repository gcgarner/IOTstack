#!/bin/bash

pushd ~/IOTstack

[ -d ./backups ] || mkdir ./backups

#create the list of files to backup
echo "./docker-compose.yml" >list.txt
echo "./services/" >>list.txt
echo "./volumes/" >>list.txt

#if influxdb folder exists then back it up
if [ -d ./volumes/influxdb ]; then
	./scripts/backup_influxdb.sh
	echo "./backups/influxdb/" >>list.txt
fi

echo "compressing stack folders"
sudo tar -czf \
	./backups/"backup-$(date +"%Y-%m-%d").tar.gz" \
	--exclude=./volumes/influxdb/* \
	-T list.txt

rm list.txt

echo "backup saved to ./backups/"backup-$(date +"%Y-%m-%d").tar.gz""

du -h ./backups/"backup-$(date +"%Y-%m-%d").tar.gz"

if [ -f ./backups/dropbox ]; then
	echo "uploading to dropbox"
	~/Dropbox-Uploader/dropbox_uploader.sh upload ./backups/"backup-$(date +"%Y-%m-%d").tar.gz" /IOTstackBU/
fi

if [ -f ./backups/rclone ]; then
	echo "uploading to Google Drive"
	rclone -P copy ./backups/"backup-$(date +"%Y-%m-%d").tar.gz" gdrive:/IOTstackBU/
fi

popd
