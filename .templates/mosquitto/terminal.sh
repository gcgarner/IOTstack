#!/bin/bash

echo "you are about to enter the shell for mosquitto"
echo "the documentation explains how to secure mosquitto with a username and password."
echo "Security Documentation: https://github.com/SensorsIot/IOTstack/blob/master/docs/Containers/Mosquitto.md#security"

docker exec -it mosquitto sh
