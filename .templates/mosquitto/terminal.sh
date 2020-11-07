#!/bin/bash

echo "You are about to enter the shell for mosquitto."
echo "The documentation explains how to secure mosquitto with a username and password."
echo "Security Documentation: https://github.com/SensorsIot/IOTstack/blob/master/docs/Containers/Mosquitto.md#security"
echo ""
echo "IOTstack mosquitto Documentation: https://sensorsiot.github.io/IOTstack/Containers/Mosquitto/"
echo ""

docker exec -it mosquitto sh
