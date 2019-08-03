#!/bin/bash

if [ ! -d $PWD/grafana ]; then
   #rm -r grafana
   mkdir grafana
   mkdir grafana/data
fi

chown -R 472:472 $PWD/grafana

if [ ! -d $PWD/nodered ]; then
   #rm -r nodered
   mkdir nodered
   mkdir nodered/data
fi

chown -R 1000:1000 $PWD/nodered
