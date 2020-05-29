#!/bin/bash

# build Dockerfile for nodered

node_selection=$(whiptail --title "Node-RED nodes" --checklist --separate-output \
	"Use the [SPACEBAR] to select the nodes you want preinstalled" 20 78 12 -- \
	"node-red-node-pi-gpiod" " " "ON" \
	"node-red-dashboard" " " "ON" \
	"node-red-contrib-influxdb" " " "ON" \
	"node-red-contrib-boolean-logic" " " "ON" \
	"node-red-node-rbe" " " "ON" \
	"node-red-configurable-ping" " " "ON" \
	"node-red-node-openweathermap" " " "OFF" \
	"node-red-contrib-discord" " " "OFF" \
	"node-red-node-email" " " "on" \
	"node-red-node-google" " " "OFF" \
	"node-red-node-emoncms" " " "OFF" \
	"node-red-node-geofence" " " "OFF" \
	"node-red-node-ping" " " "OFF" \
	"node-red-node-random" " " "OFF" \
	"node-red-node-smooth" " " "OFF" \
	"node-red-node-darksky" " " "OFF" \
	"node-red-node-sqlite" " " "OFF" \
	"node-red-contrib-config" " " "OFF" \
	"node-red-contrib-grove" " " "OFF" \
	"node-red-contrib-diode" " " "OFF" \
	"node-red-contrib-bigtimer" " " "OFF" \
	"node-red-contrib-esplogin" " " "OFF" \
	"node-red-contrib-timeout" " " "OFF" \
	"node-red-contrib-moment" " " "OFF" \
	"node-red-contrib-particle" " " "OFF" \
	"node-red-contrib-web-worldmap" " " "OFF" \
	"node-red-contrib-ramp-thermostat" " " "OFF" \
	"node-red-contrib-isonline" " " "OFF" \
	"node-red-contrib-npm" " " "OFF" \
	"node-red-contrib-file-function" " " "OFF" \
	"node-red-contrib-home-assistant-websocket" " " "OFF" \
	"node-red-contrib-blynk-ws" " " "OFF" \
	"node-red-contrib-owntracks" " " "OFF" \
	"node-red-contrib-alexa-local" " " "OFF" \
	"node-red-contrib-heater-controller" " " "OFF" \
	"node-red-contrib-deconz" " " "OFF" \
	3>&1 1>&2 2>&3)

##echo "$check_selection"
mapfile -t checked_nodes <<<"$node_selection"

nr_dfile=./services/nodered/Dockerfile

sqliteflag=0

touch $nr_dfile
echo "FROM nodered/node-red:latest" >$nr_dfile
#node red install script inspired from https://tech.scargill.net/the-script/
echo "RUN for addonnodes in \\" >>$nr_dfile
for checked in "${checked_nodes[@]}"; do
	#test to see if sqlite is selected and set flag, sqlite require additional flags
	if [ "$checked" = "node-red-node-sqlite" ]; then
		sqliteflag=1
	else
		echo "$checked \\" >>$nr_dfile
	fi
done
echo "; do \\" >>$nr_dfile
echo "npm install \${addonnodes} ;\\" >>$nr_dfile
echo "done;" >>$nr_dfile

[ $sqliteflag = 1 ] && echo "RUN npm install --unsafe-perm node-red-node-sqlite" >>$nr_dfile
