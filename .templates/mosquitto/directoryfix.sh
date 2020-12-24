#!/bin/bash

[ -d ./volumes/mosquitto ] || sudo mkdir -p ./volumes/mosquitto

#check user 1883
if [ $(grep -c 'user: \"1883\"' ./services/mosquitto/service.yml) -eq 1 ]; then
	echo "...found user 1883"
	sudo mkdir -p ./volumes/mosquitto/data/
	sudo mkdir -p ./volumes/mosquitto/log/
	sudo mkdir -p ./volumes/mosquitto/pwfile/
	sudo chown -R 1883:1883 ./volumes/mosquitto/
fi

#check user 0 legacy test
if [ $(grep -c 'user: \"0\"' ./services/mosquitto/service.yml) -eq 1 ]; then
	echo "...found user 0 setting ownership for old template"
	sudo chown -R root:root ./volumes/mosquitto/
fi
