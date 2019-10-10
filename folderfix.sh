#!/bin/bash

if [ ! -d ./grafana ]; then
   mkdir grafana
   mkdir grafana/data
fi

chown -R 472:472 ./grafana

if [ ! -d ./nodered ]; then
   mkdir nodered
   mkdir nodered/data
fi

chown -R 1000:1000 ./nodered

if [ ! -d ./influxdb ]; then
   mkdir influxdb
   mkdir influxdb/data
fi
