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

#setup variables
logfile=./backups/log.txt
backupfile="backup-$(date +"%Y-%m-%d_%H%M").tar.gz"

#compress the backups folders to archive
echo "compressing stack folders"
sudo tar -czf \
	./backups/$backupfile \
	--exclude=./volumes/influxdb/* \
	-T list.txt

rm list.txt

#setup permissions
sudo chown pi:pi ./backups/backup*
sudo chown pi:pi ./backups/log.txt

#create log file and add the backup file to it
echo "backup saved to ./backups/$backupfile"
touch $logfile
echo $backupfile >>$logfile

#show size of archive file
du -h ./backups/$backupfile

#upload to cloud
if [ -f ./backups/dropbox ]; then
	echo "uploading to dropbox"
	~/Dropbox-Uploader/dropbox_uploader.sh upload ./backups/$backupfile /IOTstackBU/
fi

if [ -f ./backups/rclone ]; then
	echo "uploading to Google Drive"
	rclone -P copy ./backups/$backupfile gdrive:/IOTstackBU/
fi

#remove older backup files
ls -t1 ./backups/backup* | tail -n +6 | xargs rm -f
echo "last five backup files are saved in ~/IOTstack/backups"

popd
