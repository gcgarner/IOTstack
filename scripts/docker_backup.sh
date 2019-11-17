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
logfile=./backups/log_local.txt
backupfile="backup-$(date +"%Y-%m-%d_%H%M").tar.gz"

#compress the backups folders to archive
echo "compressing stack folders"
sudo tar -czf \
	./backups/$backupfile \
	--exclude=./volumes/influxdb/* \
	-T list.txt

rm list.txt

#set permission for backup files
sudo chown pi:pi ./backups/backup*

#create local logfile and append the latest backup file to it
echo "backup saved to ./backups/$backupfile"
sudo touch $logfile
sudo chown pi:pi $logfile
echo $backupfile >>$logfile

#show size of archive file
du -h ./backups/$backupfile

#remove older local backup files
ls -t1 ./backups/backup* | tail -n +8 | sudo xargs rm -f
echo "last seven local backup files are saved in ~/IOTstack/backups"



#cloud related - dropbox
if [ -f ./backups/dropbox ]; then

	#setup variables
	dropboxfolder=/IOTstackBU
	dropboxuploader=~/Dropbox-Uploader/dropbox_uploader.sh
	dropboxlog=./backups/log_dropbox.txt

	#upload new backup to dropbox
	echo "uploading to dropbox"
	$dropboxuploader upload ./backups/$backupfile $dropboxfolder

	#list older files to be deleted from cloud (exludes last 7)
	echo "getting older filenames to be deleted from cloud"
	files=$($dropboxuploader list $dropboxfolder | awk {' print $3 '} | tail -n +2 | head -n -7)

	#write files to be deleted to logfile
	sudo touch $dropboxlog
	sudo chown pi:pi $dropboxlog
	echo $files | tr " " "\n" >$dropboxlog

	#delete files from cloud as per logfile
	echo "deleting files from cloud - last 7 files are kept"
	echo "if less than 7 files are in cloud you wil see FAILED message below"
	input=$dropboxlog
	while IFS= read -r file
	do
	    $dropboxuploader delete $dropboxfolder/$file
	done < "$input"

	echo "deleted from cloud" >>$dropboxlog

fi


#cloud related - google drive
if [ -f ./backups/rclone ]; then
	echo "uploading to Google Drive"
	rclone -P copy ./backups/$backupfile gdrive:/IOTstackBU/
fi



popd
