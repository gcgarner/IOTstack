#!/bin/bash

echo "you are about to enter the shell for mosquitto"
echo "to add a password: mosquitto_passwd -c /etc/mosquitto/passwd MYUSER"
echo "the command will ask for you password and confirm"
echo "to exit: exit"

docker exec -it mqtt sh
