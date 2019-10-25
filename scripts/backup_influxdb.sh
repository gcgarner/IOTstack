#!/bin/bash

#first move the contents of the old backup out and clear the directory
[ -d ~/IOTstack/backups/influxdb/db_old ] || sudo mkdir ~/IOTstack/backups/influxdb/db_old
sudo rm ~/IOTstack/backups/influxdb/db_old/*
sudo mv ~/IOTstack/backups/influxdb/db/* ~/IOTstack/backups/influxdb/db_old/
#sudo rm ~/IOTstack/backups/influxdb/db/*

#execute the backup command
docker exec -it influxdb influxd backup -portable /var/lib/influxdb/backup
