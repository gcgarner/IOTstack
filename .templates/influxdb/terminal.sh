#!/bin/bash

echo "You are about to enter the influxdb console:"
echo ""
echo "IOTstack influxdb Documentation: https://sensorsiot.github.io/IOTstack/Containers/InfluxDB/"
echo ""
echo "to create a db: CREATE DATABASE myname"
echo "to show existing a databases: SHOW DATABASES"
echo "to use a specific db: USE myname"
echo ""
echo "to exit type: EXIT"
echo ""
echo "docker exec -it influxdb influx"

docker exec -it influxdb influx "$@"
